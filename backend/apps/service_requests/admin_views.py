"""
Admin API views for service_requests app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ServiceRequest
from .serializers import ServiceRequestAdminSerializer, UserSerializer
from .tasks import send_status_update_email


class AdminServiceRequestViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for ServiceRequest model with full management capabilities."""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'service', 'assigned_to']
    search_fields = ['project_title', 'client_name', 'client_email', 'project_description']
    ordering_fields = ['created_at', 'deadline', 'priority', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get all service requests with related data."""
        return ServiceRequest.objects.select_related('service', 'assigned_to', 'service__category')
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get comprehensive dashboard statistics."""
        queryset = self.get_queryset()
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Basic counts
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'in_progress': queryset.filter(status='in_progress').count(),
            'completed': queryset.filter(status='completed').count(),
            'cancelled': queryset.filter(status='cancelled').count(),
            'overdue': len([r for r in queryset if r.is_overdue]),
            'unassigned': queryset.filter(assigned_to=None).count(),
        }
        
        # Priority breakdown
        stats['by_priority'] = {
            'low': queryset.filter(priority='low').count(),
            'normal': queryset.filter(priority='normal').count(),
            'high': queryset.filter(priority='high').count(),
            'urgent': queryset.filter(priority='urgent').count(),
        }
        
        # Time-based stats
        stats['recent'] = {
            'today': queryset.filter(created_at__date=today).count(),
            'this_week': queryset.filter(created_at__date__gte=week_ago).count(),
            'this_month': queryset.filter(created_at__date__gte=month_ago).count(),
        }
        
        # Service breakdown
        service_stats = queryset.values('service__title').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        stats['top_services'] = list(service_stats)
        
        # Assigned user breakdown
        user_stats = queryset.filter(assigned_to__isnull=False).values(
            'assigned_to__username', 'assigned_to__first_name', 'assigned_to__last_name'
        ).annotate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            completed=Count('id', filter=Q(status='completed'))
        ).order_by('-total')
        stats['by_assignee'] = list(user_stats)
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update request status with optional notes."""
        service_request = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if new_status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = service_request.status
        service_request.status = new_status
        
        if notes:
            if service_request.notes:
                service_request.notes += f"\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status changed from {old_status} to {new_status}: {notes}"
            else:
                service_request.notes = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] Status changed from {old_status} to {new_status}: {notes}"
        
        service_request.save()
        
        # Send email notification to client about status change
        if old_status != new_status:
            try:
                # Default to English for admin-initiated changes, could be enhanced to detect client's preferred language
                send_status_update_email.delay(service_request.id, old_status, new_status, 'en')
            except Exception as e:
                # Log error but don't fail the status update
                print(f"Failed to send status update email for request {service_request.id}: {e}")
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def assign_user(self, request, pk=None):
        """Assign request to a user."""
        service_request = self.get_object()
        user_id = request.data.get('user_id')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id, is_active=True)
                service_request.assigned_to = user
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            service_request.assigned_to = None
        
        service_request.save()
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_priority(self, request, pk=None):
        """Update request priority."""
        service_request = self.get_object()
        new_priority = request.data.get('priority')
        
        if new_priority not in dict(ServiceRequest.PRIORITY_CHOICES):
            return Response({'error': 'Invalid priority'}, status=status.HTTP_400_BAD_REQUEST)
        
        service_request.priority = new_priority
        service_request.save()
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_update_status(self, request):
        """Bulk update status of multiple requests."""
        request_ids = request.data.get('request_ids', [])
        new_status = request.data.get('status')
        
        if new_status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = ServiceRequest.objects.filter(id__in=request_ids).update(status=new_status)
        
        return Response({
            'message': f'{updated_count} requests updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['patch'])
    def bulk_assign(self, request):
        """Bulk assign multiple requests to a user."""
        request_ids = request.data.get('request_ids', [])
        user_id = request.data.get('user_id')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id, is_active=True)
                updated_count = ServiceRequest.objects.filter(id__in=request_ids).update(assigned_to=user)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            updated_count = ServiceRequest.objects.filter(id__in=request_ids).update(assigned_to=None)
        
        return Response({
            'message': f'{updated_count} requests updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue requests."""
        queryset = self.get_queryset()
        overdue_requests = [r for r in queryset if r.is_overdue]
        serializer = self.get_serializer(overdue_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unassigned(self, request):
        """Get unassigned requests."""
        unassigned_requests = self.get_queryset().filter(assigned_to=None)
        serializer = self.get_serializer(unassigned_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Perform bulk actions on multiple requests."""
        request_ids = request.data.get('request_ids', [])
        action_type = request.data.get('type')
        action_data = request.data.get('data', {})
        
        if not request_ids:
            return Response({'error': 'No request IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = ServiceRequest.objects.filter(id__in=request_ids)
        updated_count = 0
        
        if action_type == 'status':
            new_status = action_data.get('status')
            if new_status in dict(ServiceRequest.STATUS_CHOICES):
                updated_count = queryset.update(status=new_status)
        
        elif action_type == 'priority':
            new_priority = action_data.get('priority')
            if new_priority in dict(ServiceRequest.PRIORITY_CHOICES):
                updated_count = queryset.update(priority=new_priority)
        
        elif action_type == 'assign':
            user_id = action_data.get('assigned_to')
            if user_id:
                try:
                    user = User.objects.get(id=user_id, is_active=True)
                    updated_count = queryset.update(assigned_to=user)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                updated_count = queryset.update(assigned_to=None)
        
        elif action_type == 'delete':
            updated_count = queryset.count()
            queryset.delete()
        
        else:
            return Response({'error': 'Invalid action type'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': f'{updated_count} requests updated successfully',
            'updated_count': updated_count
        })


class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin ViewSet for User model (read-only for assignment purposes)."""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    
    @action(detail=False, methods=['get'])
    def staff(self, request):
        """Get staff users only."""
        staff_users = self.get_queryset().filter(is_staff=True)
        serializer = self.get_serializer(staff_users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def workload(self, request, pk=None):
        """Get workload statistics for a user."""
        user = self.get_object()
        requests = ServiceRequest.objects.filter(assigned_to=user)
        
        workload = {
            'user': self.get_serializer(user).data,
            'total_assigned': requests.count(),
            'pending': requests.filter(status='pending').count(),
            'in_progress': requests.filter(status='in_progress').count(),
            'completed': requests.filter(status='completed').count(),
            'overdue': len([r for r in requests if r.is_overdue]),
        }
        
        return Response(workload)
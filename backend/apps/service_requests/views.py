"""
Views for service_requests app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer, ServiceRequestAdminSerializer, UserSerializer


class ServiceRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for ServiceRequest model."""
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'service', 'assigned_to']
    search_fields = ['project_title', 'client_name', 'client_email', 'project_description']
    ordering_fields = ['created_at', 'deadline', 'priority']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            # Allow anyone to create service requests
            permission_classes = [permissions.AllowAny]
        else:
            # Only staff can view/manage requests
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action and user permissions."""
        if self.action == 'create':
            from .serializers import ServiceRequestPublicSerializer
            return ServiceRequestPublicSerializer
        elif self.request.user.is_staff:
            return ServiceRequestAdminSerializer
        return ServiceRequestSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = ServiceRequest.objects.select_related('service', 'assigned_to')
        if not self.request.user.is_staff:
            # Public users can't view existing requests, only create new ones
            return queryset.none()
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new service request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set default values for admin fields
        service_request = serializer.save(
            status='pending',
            priority='normal'
        )
        
        # Return success response without sensitive data
        return Response({
            'message': 'Service request submitted successfully',
            'request_id': service_request.id,
            'project_title': service_request.project_title
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for admin."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'in_progress': queryset.filter(status='in_progress').count(),
            'completed': queryset.filter(status='completed').count(),
            'cancelled': queryset.filter(status='cancelled').count(),
            'overdue': len([r for r in queryset if r.is_overdue]),
        }
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update request status."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        service_request = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        service_request.status = new_status
        service_request.save()
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def assign_user(self, request, pk=None):
        """Assign request to a user."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        service_request = self.get_object()
        user_id = request.data.get('user_id')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                service_request.assigned_to = user
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            service_request.assigned_to = None
        
        service_request.save()
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model (read-only for assignment purposes)."""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
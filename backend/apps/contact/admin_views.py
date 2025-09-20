"""
Admin API views for contact app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import ContactInquiry
from .serializers import ContactInquiryAdminSerializer


class AdminContactInquiryViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for ContactInquiry model with full management capabilities."""
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquiryAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inquiry_type', 'is_read', 'is_responded']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'name', 'subject']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get comprehensive dashboard statistics."""
        queryset = self.get_queryset()
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        stats = {
            'total': queryset.count(),
            'unread': queryset.filter(is_read=False).count(),
            'pending_response': queryset.filter(is_responded=False).count(),
            'responded': queryset.filter(is_responded=True).count(),
        }
        
        # Time-based stats
        stats['recent'] = {
            'today': queryset.filter(created_at__date=today).count(),
            'this_week': queryset.filter(created_at__date__gte=week_ago).count(),
            'this_month': queryset.filter(created_at__date__gte=month_ago).count(),
        }
        
        # Inquiry type breakdown
        stats['by_type'] = {}
        for choice_value, choice_label in ContactInquiry.INQUIRY_TYPES:
            type_count = queryset.filter(inquiry_type=choice_value).count()
            stats['by_type'][choice_value] = {
                'label': choice_label,
                'count': type_count,
                'unread': queryset.filter(inquiry_type=choice_value, is_read=False).count(),
                'pending_response': queryset.filter(inquiry_type=choice_value, is_responded=False).count()
            }
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        """Mark inquiry as read."""
        inquiry = self.get_object()
        inquiry.is_read = True
        inquiry.save()
        
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_responded(self, request, pk=None):
        """Mark inquiry as responded with optional notes."""
        inquiry = self.get_object()
        inquiry.is_responded = True
        inquiry.is_read = True  # Mark as read when responding
        
        response_notes = request.data.get('response_notes', '')
        if response_notes:
            if inquiry.response_notes:
                inquiry.response_notes += f"\n\n[{timezone.now().strftime('%Y-%m-%d %H:%M')}] {response_notes}"
            else:
                inquiry.response_notes = f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}] {response_notes}"
        
        inquiry.save()
        
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_mark_read(self, request):
        """Mark multiple inquiries as read."""
        inquiry_ids = request.data.get('inquiry_ids', [])
        updated_count = ContactInquiry.objects.filter(id__in=inquiry_ids).update(is_read=True)
        
        return Response({
            'message': f'{updated_count} inquiries marked as read',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['patch'])
    def bulk_mark_responded(self, request):
        """Mark multiple inquiries as responded."""
        inquiry_ids = request.data.get('inquiry_ids', [])
        updated_count = ContactInquiry.objects.filter(id__in=inquiry_ids).update(
            is_responded=True,
            is_read=True
        )
        
        return Response({
            'message': f'{updated_count} inquiries marked as responded',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread inquiries."""
        unread_inquiries = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread_inquiries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_response(self, request):
        """Get inquiries pending response."""
        pending_inquiries = self.get_queryset().filter(is_responded=False)
        serializer = self.get_serializer(pending_inquiries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get inquiries grouped by type."""
        inquiry_type = request.query_params.get('type')
        
        if inquiry_type and inquiry_type in dict(ContactInquiry.INQUIRY_TYPES):
            inquiries = self.get_queryset().filter(inquiry_type=inquiry_type)
            serializer = self.get_serializer(inquiries, many=True)
            return Response(serializer.data)
        else:
            # Return all types with counts
            result = {}
            for choice_value, choice_label in ContactInquiry.INQUIRY_TYPES:
                inquiries = self.get_queryset().filter(inquiry_type=choice_value)
                result[choice_value] = {
                    'label': choice_label,
                    'count': inquiries.count(),
                    'inquiries': self.get_serializer(inquiries, many=True).data
                }
            return Response(result)
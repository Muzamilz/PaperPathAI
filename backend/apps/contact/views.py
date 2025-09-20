"""
Views for contact app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContactInquiry
from .serializers import ContactInquirySerializer, ContactInquiryAdminSerializer


class ContactInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for ContactInquiry model."""
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inquiry_type', 'is_read', 'is_responded']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'name', 'subject']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            # Allow anyone to create contact inquiries
            permission_classes = [permissions.AllowAny]
        else:
            # Only staff can view/manage inquiries
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action and user permissions."""
        if self.action == 'create':
            from .serializers import ContactInquiryPublicSerializer
            return ContactInquiryPublicSerializer
        elif self.request.user.is_staff:
            return ContactInquiryAdminSerializer
        return ContactInquirySerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new contact inquiry."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set default values for admin fields
        contact_inquiry = serializer.save(
            is_read=False,
            is_responded=False
        )
        
        # Return success response without sensitive data
        return Response({
            'message': 'Contact inquiry submitted successfully',
            'inquiry_id': contact_inquiry.id,
            'subject': contact_inquiry.subject
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for admin."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'unread': queryset.filter(is_read=False).count(),
            'pending_response': queryset.filter(is_responded=False).count(),
            'by_type': {}
        }
        
        # Count by inquiry type
        for choice_value, choice_label in ContactInquiry.INQUIRY_TYPES:
            stats['by_type'][choice_value] = {
                'label': choice_label,
                'count': queryset.filter(inquiry_type=choice_value).count()
            }
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        """Mark inquiry as read."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        inquiry = self.get_object()
        inquiry.is_read = True
        inquiry.save()
        
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_responded(self, request, pk=None):
        """Mark inquiry as responded."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        inquiry = self.get_object()
        inquiry.is_responded = True
        response_notes = request.data.get('response_notes', '')
        if response_notes:
            inquiry.response_notes = response_notes
        inquiry.save()
        
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_mark_read(self, request):
        """Mark multiple inquiries as read."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        inquiry_ids = request.data.get('ids', [])
        updated_count = ContactInquiry.objects.filter(id__in=inquiry_ids).update(is_read=True)
        
        return Response({'updated_count': updated_count})
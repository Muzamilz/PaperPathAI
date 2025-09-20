"""
Public API views for contact app.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import ContactInquiry
from .serializers import ContactInquiryPublicSerializer


class PublicContactInquiryViewSet(viewsets.ModelViewSet):
    """Public ViewSet for ContactInquiry model (create-only)."""
    queryset = ContactInquiry.objects.none()  # Public users can't view existing inquiries
    serializer_class = ContactInquiryPublicSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']  # Only allow POST (create) operations
    
    def create(self, request, *args, **kwargs):
        """Create a new contact inquiry."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set default values for admin fields
        contact_inquiry = serializer.save(
            is_read=False,
            is_responded=False
        )
        
        # TODO: Send email notification to admin
        # This will be implemented in task 8.1
        
        # Return success response without sensitive data
        return Response({
            'message': 'Contact inquiry submitted successfully',
            'inquiry_id': contact_inquiry.id,
            'subject': contact_inquiry.subject,
            'inquiry_type': contact_inquiry.get_inquiry_type_display()
        }, status=status.HTTP_201_CREATED)
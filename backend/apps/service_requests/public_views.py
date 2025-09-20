"""
Public API views for service_requests app.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import ServiceRequest
from .serializers import ServiceRequestPublicSerializer
from .tasks import send_request_confirmation_email, send_admin_notification_email


class PublicServiceRequestViewSet(viewsets.ModelViewSet):
    """Public ViewSet for ServiceRequest model (create-only)."""
    queryset = ServiceRequest.objects.none()  # Public users can't view existing requests
    serializer_class = ServiceRequestPublicSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']  # Only allow POST (create) operations
    
    def create(self, request, *args, **kwargs):
        """Create a new service request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set default values for admin fields
        service_request = serializer.save(
            status='pending',
            priority='normal'
        )
        
        # Get language from request headers or default to 'en'
        language = request.headers.get('Accept-Language', 'en')
        if language.startswith('ar'):
            language = 'ar'
        else:
            language = 'en'
        
        # Send email notifications asynchronously
        try:
            # Send confirmation email to client
            send_request_confirmation_email.delay(service_request.id, language)
            
            # Send notification to admin (urgent if high priority)
            notification_type = 'urgent_request' if service_request.priority in ['high', 'urgent'] else 'new_request'
            send_admin_notification_email.delay(service_request.id, notification_type)
        except Exception as e:
            # Log error but don't fail the request creation
            print(f"Failed to send email notifications for request {service_request.id}: {e}")
        
        # Return success response without sensitive data
        return Response({
            'message': 'Service request submitted successfully',
            'request_id': service_request.id,
            'project_title': service_request.project_title,
            'service': service_request.service.title,
            'status': 'pending'
        }, status=status.HTTP_201_CREATED)
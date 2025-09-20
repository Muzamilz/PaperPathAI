"""
API views for email notification management.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import ServiceRequest
from .email_tracking import get_email_stats, EmailNotification
from .tasks import (
    send_request_confirmation_email,
    send_status_update_email,
    send_admin_notification_email
)


class EmailNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for email notification tracking (admin only)."""
    
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return EmailNotification.objects.all()
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get email notification statistics."""
        days = request.query_params.get('days', 30)
        try:
            days = int(days)
        except (ValueError, TypeError):
            days = 30
        
        stats = get_email_stats(days=days)
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def recent_failures(self, request):
        """Get recent failed email notifications."""
        failed_notifications = EmailNotification.objects.filter(
            status='failed'
        ).order_by('-created_at')[:20]
        
        failures = []
        for notification in failed_notifications:
            failures.append({
                'id': notification.id,
                'service_request_id': notification.service_request.id,
                'project_title': notification.service_request.project_title,
                'email_type': notification.get_email_type_display(),
                'recipient': notification.recipient_email,
                'error_message': notification.error_message,
                'created_at': notification.created_at,
            })
        
        return Response(failures)
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """Retry a failed email notification."""
        try:
            notification = EmailNotification.objects.get(pk=pk)
        except EmailNotification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if notification.status != 'failed':
            return Response(
                {'error': 'Can only retry failed notifications'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Retry the appropriate email task
        try:
            if notification.email_type == 'confirmation':
                task = send_request_confirmation_email.delay(
                    notification.service_request.id, 
                    notification.language
                )
            elif notification.email_type == 'status_update':
                # For retry, we'll use current status as both old and new
                current_status = notification.service_request.status
                task = send_status_update_email.delay(
                    notification.service_request.id,
                    current_status,
                    current_status,
                    notification.language
                )
            elif notification.email_type in ['admin_notification', 'overdue_alert', 'urgent_alert']:
                notification_type = 'new_request'
                if notification.email_type == 'overdue_alert':
                    notification_type = 'overdue_request'
                elif notification.email_type == 'urgent_alert':
                    notification_type = 'urgent_request'
                
                task = send_admin_notification_email.delay(
                    notification.service_request.id,
                    notification_type
                )
            else:
                return Response(
                    {'error': 'Unknown email type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update the notification record
            notification.status = 'queued'
            notification.celery_task_id = task.id
            notification.error_message = ''
            notification.save()
            
            return Response({
                'message': 'Email notification retry queued successfully',
                'task_id': task.id
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to retry email: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmailTestViewSet(viewsets.ViewSet):
    """ViewSet for testing email functionality (admin only)."""
    
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['post'])
    def send_test_email(self, request):
        """Send a test email notification."""
        email_type = request.data.get('email_type', 'confirmation')
        language = request.data.get('language', 'en')
        request_id = request.data.get('request_id')
        
        if not request_id:
            # Use the most recent request
            service_request = ServiceRequest.objects.first()
            if not service_request:
                return Response(
                    {'error': 'No service requests found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                service_request = ServiceRequest.objects.get(id=request_id)
            except ServiceRequest.DoesNotExist:
                return Response(
                    {'error': 'Service request not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        try:
            if email_type == 'confirmation':
                task = send_request_confirmation_email.delay(service_request.id, language)
            elif email_type == 'status_update':
                task = send_status_update_email.delay(
                    service_request.id, 
                    'pending', 
                    'in_progress', 
                    language
                )
            elif email_type == 'admin_notification':
                task = send_admin_notification_email.delay(service_request.id, 'new_request')
            else:
                return Response(
                    {'error': 'Invalid email type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'message': f'Test {email_type} email queued successfully',
                'task_id': task.id,
                'service_request': {
                    'id': service_request.id,
                    'project_title': service_request.project_title,
                    'client_email': service_request.client_email,
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to send test email: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
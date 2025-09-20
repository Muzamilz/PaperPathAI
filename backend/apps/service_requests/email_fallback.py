"""
Fallback email service for deployments without Celery/Redis.
This sends emails synchronously when background tasks aren't available.
"""
from django.conf import settings
from .email_service import email_service
import logging

logger = logging.getLogger(__name__)


def send_email_sync(template_type, language, context, recipient_list, notification_type=None):
    """
    Send email synchronously (fallback when Celery is not available).
    
    Args:
        template_type (str): Type of email template
        language (str): Language code ('en' or 'ar')
        context (dict): Context variables for template
        recipient_list (list): List of recipient email addresses
        notification_type (str): Optional notification type for admin emails
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        result = email_service.send_email(
            template_type=template_type,
            language=language,
            context=context,
            recipient_list=recipient_list,
            notification_type=notification_type
        )
        logger.info(f"Email sent successfully: {template_type} to {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {template_type} to {recipient_list}. Error: {e}")
        return False


def send_request_confirmation_email_sync(request_id, language='en'):
    """Send confirmation email synchronously."""
    from .models import ServiceRequest
    
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        context = {
            'client_name': service_request.client_name,
            'service_name': service_request.service.title,
            'project_title': service_request.project_title,
            'request_id': service_request.id,
            'created_at': service_request.created_at.strftime('%Y-%m-%d %H:%M'),
            'deadline': service_request.deadline.strftime('%Y-%m-%d'),
            'budget': service_request.budget,
            'client_phone': service_request.client_phone or 'Not provided',
        }
        
        return send_email_sync(
            template_type='request_confirmation',
            language=language,
            context=context,
            recipient_list=[service_request.client_email]
        )
        
    except ServiceRequest.DoesNotExist:
        logger.error(f"ServiceRequest with id {request_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Error sending confirmation email for request {request_id}: {e}")
        return False


def send_status_update_email_sync(request_id, old_status, new_status, language='en'):
    """Send status update email synchronously."""
    from .models import ServiceRequest
    
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        # Get status display names
        status_display = dict(ServiceRequest.STATUS_CHOICES)
        
        context = {
            'client_name': service_request.client_name,
            'service_name': service_request.service.title,
            'project_title': service_request.project_title,
            'request_id': service_request.id,
            'old_status': status_display.get(old_status, old_status),
            'new_status': status_display.get(new_status, new_status),
        }
        
        return send_email_sync(
            template_type='status_update',
            language=language,
            context=context,
            recipient_list=[service_request.client_email]
        )
        
    except ServiceRequest.DoesNotExist:
        logger.error(f"ServiceRequest with id {request_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Error sending status update email for request {request_id}: {e}")
        return False


def send_admin_notification_email_sync(request_id, notification_type='new_request'):
    """Send admin notification email synchronously."""
    from .models import ServiceRequest
    from django.contrib.auth.models import User
    
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        # Get admin users (staff users)
        admin_emails = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))
        admin_emails = [email for email in admin_emails if email]  # Filter out empty emails
        
        if not admin_emails:
            logger.warning("No admin emails found")
            return False
        
        context = {
            'client_name': service_request.client_name,
            'client_email': service_request.client_email,
            'client_phone': service_request.client_phone or 'Not provided',
            'service_name': service_request.service.title,
            'project_title': service_request.project_title,
            'project_description': service_request.project_description,
            'priority': service_request.get_priority_display(),
            'deadline': service_request.deadline.strftime('%Y-%m-%d'),
            'budget': service_request.budget,
            'request_id': service_request.id,
            'created_at': service_request.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        
        return send_email_sync(
            template_type='admin_notification',
            language='en',  # Admin emails always in English
            context=context,
            recipient_list=admin_emails,
            notification_type=notification_type
        )
        
    except ServiceRequest.DoesNotExist:
        logger.error(f"ServiceRequest with id {request_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Error sending admin notification for request {request_id}: {e}")
        return False
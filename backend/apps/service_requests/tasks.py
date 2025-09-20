"""
Celery tasks for service request email notifications.
"""
from celery import shared_task
from django.contrib.auth.models import User
from .models import ServiceRequest
from .email_service import email_service


@shared_task(bind=True, max_retries=3)
def send_request_confirmation_email(self, request_id, language='en'):
    """
    Send confirmation email to client when a service request is submitted.
    
    Args:
        request_id (int): ID of the ServiceRequest
        language (str): Language code for email template ('en' or 'ar')
    """
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        # Prepare context for email template
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
        
        # Send email using the email service
        email_service.send_email(
            template_type='request_confirmation',
            language=language,
            context=context,
            recipient_list=[service_request.client_email]
        )
        
        return f"Confirmation email sent to {service_request.client_email}"
        
    except ServiceRequest.DoesNotExist:
        raise Exception(f"ServiceRequest with id {request_id} does not exist")
    except Exception as exc:
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_status_update_email(self, request_id, old_status, new_status, language='en'):
    """
    Send email notification when service request status changes.
    
    Args:
        request_id (int): ID of the ServiceRequest
        old_status (str): Previous status
        new_status (str): New status
        language (str): Language code for email template ('en' or 'ar')
    """
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        # Get status display names
        status_display = dict(ServiceRequest.STATUS_CHOICES)
        
        # Prepare context for email template
        context = {
            'client_name': service_request.client_name,
            'service_name': service_request.service.title,
            'project_title': service_request.project_title,
            'request_id': service_request.id,
            'old_status': status_display.get(old_status, old_status),
            'new_status': status_display.get(new_status, new_status),
        }
        
        # Send email using the email service
        email_service.send_email(
            template_type='status_update',
            language=language,
            context=context,
            recipient_list=[service_request.client_email]
        )
        
        return f"Status update email sent to {service_request.client_email}"
        
    except ServiceRequest.DoesNotExist:
        raise Exception(f"ServiceRequest with id {request_id} does not exist")
    except Exception as exc:
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_admin_notification_email(self, request_id, notification_type='new_request'):
    """
    Send notification email to admin staff about service requests.
    
    Args:
        request_id (int): ID of the ServiceRequest
        notification_type (str): Type of notification ('new_request', 'urgent_request', etc.)
    """
    try:
        service_request = ServiceRequest.objects.select_related('service').get(id=request_id)
        
        # Get admin users (staff users)
        admin_emails = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))
        admin_emails = [email for email in admin_emails if email]  # Filter out empty emails
        
        if not admin_emails:
            return "No admin emails found"
        
        # Prepare context for email template
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
        
        # Send email using the email service (admin emails are always in English)
        email_service.send_email(
            template_type='admin_notification',
            language='en',
            context=context,
            recipient_list=admin_emails,
            notification_type=notification_type
        )
        
        return f"Admin notification sent to {len(admin_emails)} recipients"
        
    except ServiceRequest.DoesNotExist:
        raise Exception(f"ServiceRequest with id {request_id} does not exist")
    except Exception as exc:
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def send_daily_overdue_notifications():
    """
    Daily task to send notifications about overdue requests.
    This task should be scheduled to run daily via Celery Beat.
    """
    from django.utils import timezone
    
    # Get overdue requests
    overdue_requests = ServiceRequest.objects.filter(
        deadline__lt=timezone.now().date(),
        status__in=['pending', 'in_progress']
    ).select_related('service')
    
    notifications_sent = 0
    
    for request in overdue_requests:
        try:
            # Send admin notification for overdue request
            send_admin_notification_email.delay(request.id, 'overdue_request')
            notifications_sent += 1
        except Exception as e:
            # Log error but continue with other requests
            print(f"Failed to send overdue notification for request {request.id}: {e}")
    
    return f"Sent {notifications_sent} overdue notifications"


@shared_task
def cleanup_old_attachments():
    """
    Cleanup task to remove old request attachments.
    This task should be scheduled to run weekly via Celery Beat.
    """
    import os
    from django.utils import timezone
    from datetime import timedelta
    
    # Remove attachments from requests older than 1 year and completed/cancelled
    cutoff_date = timezone.now() - timedelta(days=365)
    old_requests = ServiceRequest.objects.filter(
        created_at__lt=cutoff_date,
        status__in=['completed', 'cancelled'],
        attachments__isnull=False
    )
    
    files_removed = 0
    
    for request in old_requests:
        if request.attachments and os.path.exists(request.attachments.path):
            try:
                os.remove(request.attachments.path)
                request.attachments = None
                request.save()
                files_removed += 1
            except Exception as e:
                print(f"Failed to remove attachment for request {request.id}: {e}")
    
    return f"Removed {files_removed} old attachment files"
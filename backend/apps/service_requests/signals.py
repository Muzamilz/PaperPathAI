"""
Django signals for automatic email notifications.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ServiceRequest
from django.conf import settings
from .tasks import send_status_update_email, send_admin_notification_email
from .email_fallback import send_status_update_email_sync, send_admin_notification_email_sync


@receiver(pre_save, sender=ServiceRequest)
def capture_old_status(sender, instance, **kwargs):
    """Capture the old status before saving to compare with new status."""
    if instance.pk:
        try:
            old_instance = ServiceRequest.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except ServiceRequest.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=ServiceRequest)
def send_automatic_notifications(sender, instance, created, **kwargs):
    """
    Send automatic email notifications when service requests are created or updated.
    """
    if created:
        # New request created - admin notification is handled in the view
        # to include language preference from the request
        pass
    else:
        # Request updated - check if status changed
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            # Status changed - send notification to client
            try:
                if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', True):
                    # Send email synchronously (for free tier deployment)
                    send_status_update_email_sync(instance.id, old_status, instance.status, 'en')
                else:
                    # Send email asynchronously (when Redis/Celery available)
                    send_status_update_email.delay(instance.id, old_status, instance.status, 'en')
            except Exception as e:
                # Log error but don't fail the save operation
                print(f"Failed to send status update email for request {instance.id}: {e}")


@receiver(post_save, sender=ServiceRequest)
def check_urgent_notifications(sender, instance, created, **kwargs):
    """
    Check for urgent notifications that need to be sent.
    """
    if not created:
        # Check if request became overdue
        if instance.is_overdue and instance.status in ['pending', 'in_progress']:
            # Send overdue notification to admin
            try:
                if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', True):
                    send_admin_notification_email_sync(instance.id, 'overdue_request')
                else:
                    send_admin_notification_email.delay(instance.id, 'overdue_request')
            except Exception as e:
                print(f"Failed to send overdue notification for request {instance.id}: {e}")
        
        # Check if priority was changed to urgent
        old_priority = getattr(instance, '_old_priority', None)
        if old_priority and old_priority != 'urgent' and instance.priority == 'urgent':
            # Send urgent notification to admin
            try:
                if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', True):
                    send_admin_notification_email_sync(instance.id, 'urgent_request')
                else:
                    send_admin_notification_email.delay(instance.id, 'urgent_request')
            except Exception as e:
                print(f"Failed to send urgent notification for request {instance.id}: {e}")


@receiver(pre_save, sender=ServiceRequest)
def capture_old_priority(sender, instance, **kwargs):
    """Capture the old priority before saving to compare with new priority."""
    if instance.pk:
        try:
            old_instance = ServiceRequest.objects.get(pk=instance.pk)
            instance._old_priority = old_instance.priority
        except ServiceRequest.DoesNotExist:
            instance._old_priority = None
    else:
        instance._old_priority = None
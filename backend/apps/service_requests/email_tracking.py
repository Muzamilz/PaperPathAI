"""
Email tracking system for monitoring sent notifications.
"""
from django.db import models
from django.contrib.auth.models import User
from .models import ServiceRequest


class EmailNotification(models.Model):
    """Track sent email notifications."""
    
    EMAIL_TYPES = [
        ('confirmation', 'Request Confirmation'),
        ('status_update', 'Status Update'),
        ('admin_notification', 'Admin Notification'),
        ('overdue_alert', 'Overdue Alert'),
        ('urgent_alert', 'Urgent Alert'),
    ]
    
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    
    service_request = models.ForeignKey(
        ServiceRequest, 
        on_delete=models.CASCADE, 
        related_name='email_notifications'
    )
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    recipient_email = models.EmailField()
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('ar', 'Arabic')], default='en')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    celery_task_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Email Notification'
        verbose_name_plural = 'Email Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_email_type_display()} to {self.recipient_email} - {self.get_status_display()}"


def track_email_notification(service_request, email_type, recipient_email, language='en', 
                           subject='', celery_task_id='', status='queued'):
    """
    Create an email tracking record.
    
    Args:
        service_request: ServiceRequest instance
        email_type: Type of email being sent
        recipient_email: Email address of recipient
        language: Language of the email
        subject: Email subject line
        celery_task_id: Celery task ID for tracking
        status: Initial status of the email
    
    Returns:
        EmailNotification instance
    """
    return EmailNotification.objects.create(
        service_request=service_request,
        email_type=email_type,
        recipient_email=recipient_email,
        language=language,
        subject=subject,
        celery_task_id=celery_task_id,
        status=status
    )


def update_email_status(celery_task_id, status, error_message='', sent_at=None):
    """
    Update the status of an email notification.
    
    Args:
        celery_task_id: Celery task ID
        status: New status
        error_message: Error message if failed
        sent_at: Timestamp when email was sent
    """
    try:
        notification = EmailNotification.objects.get(celery_task_id=celery_task_id)
        notification.status = status
        if error_message:
            notification.error_message = error_message
        if sent_at:
            notification.sent_at = sent_at
        notification.save()
        return notification
    except EmailNotification.DoesNotExist:
        return None


def get_email_stats(service_request=None, days=30):
    """
    Get email statistics.
    
    Args:
        service_request: Optional ServiceRequest to filter by
        days: Number of days to look back
    
    Returns:
        Dictionary with email statistics
    """
    from django.utils import timezone
    from datetime import timedelta
    
    queryset = EmailNotification.objects.all()
    
    if service_request:
        queryset = queryset.filter(service_request=service_request)
    
    if days:
        cutoff_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=cutoff_date)
    
    stats = {
        'total': queryset.count(),
        'sent': queryset.filter(status='sent').count(),
        'failed': queryset.filter(status='failed').count(),
        'queued': queryset.filter(status='queued').count(),
        'bounced': queryset.filter(status='bounced').count(),
    }
    
    # Email type breakdown
    stats['by_type'] = {}
    for email_type, display_name in EmailNotification.EMAIL_TYPES:
        stats['by_type'][email_type] = queryset.filter(email_type=email_type).count()
    
    # Language breakdown
    stats['by_language'] = {
        'en': queryset.filter(language='en').count(),
        'ar': queryset.filter(language='ar').count(),
    }
    
    return stats
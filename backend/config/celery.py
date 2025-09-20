"""
Celery configuration for student services website.
"""
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('student_services')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Optional configuration, see the application user guide.
app.conf.update(
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_backend='redis://localhost:6379/0' if not settings.DEBUG else None,
    broker_url='redis://localhost:6379/0' if not settings.DEBUG else None,
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    task_routes={
        'apps.service_requests.tasks.send_request_confirmation_email': {'queue': 'emails'},
        'apps.service_requests.tasks.send_status_update_email': {'queue': 'emails'},
        'apps.service_requests.tasks.send_admin_notification_email': {'queue': 'emails'},
        'apps.service_requests.tasks.send_daily_overdue_notifications': {'queue': 'maintenance'},
        'apps.service_requests.tasks.cleanup_old_attachments': {'queue': 'maintenance'},
    },
    task_default_queue='default',
    task_queues={
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
        'emails': {
            'exchange': 'emails',
            'routing_key': 'emails',
        },
        'maintenance': {
            'exchange': 'maintenance',
            'routing_key': 'maintenance',
        },
    },
    # Periodic task schedule (Celery Beat)
    beat_schedule={
        'send-daily-overdue-notifications': {
            'task': 'apps.service_requests.tasks.send_daily_overdue_notifications',
            'schedule': 60.0 * 60.0 * 24.0,  # Run daily (24 hours)
            'options': {'queue': 'maintenance'}
        },
        'cleanup-old-attachments': {
            'task': 'apps.service_requests.tasks.cleanup_old_attachments',
            'schedule': 60.0 * 60.0 * 24.0 * 7.0,  # Run weekly (7 days)
            'options': {'queue': 'maintenance'}
        },
    },
)

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
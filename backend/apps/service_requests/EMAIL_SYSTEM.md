# Email Notification System

This document describes the email notification system for the Student Services website.

## Overview

The email system provides automated notifications for service requests with multilingual support (English and Arabic). It uses Celery for background task processing and includes comprehensive tracking and retry capabilities.

## Features

- **Multilingual Support**: Templates in both English and Arabic with proper RTL support
- **Automatic Notifications**: Triggered by service request events (creation, status changes)
- **Background Processing**: Uses Celery for reliable email delivery
- **Email Tracking**: Tracks sent emails with status monitoring
- **Retry Mechanism**: Automatic retry for failed emails with exponential backoff
- **Periodic Tasks**: Daily overdue notifications and maintenance tasks
- **Admin Interface**: Email management and testing tools

## Email Types

### 1. Request Confirmation
- **Trigger**: When a new service request is submitted
- **Recipients**: Client who submitted the request
- **Languages**: English and Arabic (based on client preference)
- **Content**: Request details, tracking information, next steps

### 2. Status Update
- **Trigger**: When request status changes (pending → in_progress → completed)
- **Recipients**: Client who submitted the request
- **Languages**: English and Arabic
- **Content**: Status change notification with context-specific messages

### 3. Admin Notification
- **Trigger**: New requests, urgent requests, overdue alerts
- **Recipients**: All active admin users
- **Languages**: English only
- **Content**: Request details, priority indicators, admin dashboard links

## Technical Implementation

### Email Service (`email_service.py`)
- Centralized email template management
- HTML email generation with responsive design
- Context-aware template formatting
- Language-specific content handling

### Celery Tasks (`tasks.py`)
- `send_request_confirmation_email`: Client confirmation emails
- `send_status_update_email`: Status change notifications
- `send_admin_notification_email`: Admin alerts
- `send_daily_overdue_notifications`: Daily maintenance task
- `cleanup_old_attachments`: Weekly cleanup task

### Django Signals (`signals.py`)
- Automatic email triggering on model changes
- Status change detection
- Priority escalation handling

### Email Tracking (`email_tracking.py`)
- Email delivery status tracking
- Statistics and reporting
- Failed email identification

## Configuration

### Django Settings
```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@studentservices.com'

# Frontend URL for email links
FRONTEND_URL = 'https://your-domain.com'
```

### Celery Configuration
```python
# Celery Beat Schedule (in celery.py)
beat_schedule={
    'send-daily-overdue-notifications': {
        'task': 'apps.service_requests.tasks.send_daily_overdue_notifications',
        'schedule': 60.0 * 60.0 * 24.0,  # Daily
    },
    'cleanup-old-attachments': {
        'task': 'apps.service_requests.tasks.cleanup_old_attachments',
        'schedule': 60.0 * 60.0 * 24.0 * 7.0,  # Weekly
    },
}
```

## Usage

### Testing Email System
```bash
# Test all email types
python manage.py test_email_notifications

# Test specific email type
python manage.py test_email_notifications --email-type=confirmation --language=ar

# Test with specific request
python manage.py test_email_notifications --request-id=123
```

### Daily Maintenance
```bash
# Run daily notifications (can be scheduled as cron job)
python manage.py send_daily_notifications

# Dry run to see what would be done
python manage.py send_daily_notifications --dry-run
```

### Starting Celery Workers
```bash
# Start Celery worker
celery -A config worker -l info

# Start Celery beat scheduler (for periodic tasks)
celery -A config beat -l info

# Start both worker and beat
celery -A config worker -B -l info
```

## API Endpoints

### Admin Email Management
- `GET /api/service-requests/admin/email-notifications/` - List email notifications
- `GET /api/service-requests/admin/email-notifications/stats/` - Email statistics
- `GET /api/service-requests/admin/email-notifications/recent_failures/` - Recent failures
- `POST /api/service-requests/admin/email-notifications/{id}/retry/` - Retry failed email

### Email Testing
- `POST /api/service-requests/admin/email-test/send_test_email/` - Send test email

## Email Templates

Templates are defined in `email_service.py` and include:

### Structure
- **Subject**: Dynamic subject line with context variables
- **Greeting**: Personalized greeting
- **Body**: Main content with formatted details
- **Footer**: Standard footer with contact information

### Styling
- Responsive HTML design
- RTL support for Arabic content
- Professional styling with brand colors
- Mobile-friendly layout

### Context Variables
- `{client_name}`: Client's name
- `{project_title}`: Project title
- `{service_name}`: Service name
- `{request_id}`: Request ID
- `{tracking_url}`: Link to track request
- `{admin_url}`: Admin dashboard link

## Monitoring and Troubleshooting

### Email Status Tracking
- All emails are tracked in the `EmailNotification` model
- Status: queued → sent/failed/bounced
- Error messages are stored for failed emails
- Retry mechanism with exponential backoff

### Common Issues
1. **SMTP Configuration**: Verify email settings in Django settings
2. **Celery Not Running**: Ensure Celery worker is active
3. **Redis Connection**: Check Redis server for Celery broker
4. **Template Errors**: Check email service logs for formatting issues

### Logs
- Celery task logs: Check worker output
- Django logs: Email backend errors
- Email tracking: Database records of all attempts

## Security Considerations

- Email addresses are validated before sending
- No sensitive information in email content
- Secure SMTP connection (TLS)
- Rate limiting on email sending
- Admin-only access to email management

## Future Enhancements

- Email template editor in admin interface
- A/B testing for email content
- Email analytics and open tracking
- SMS notifications integration
- Advanced scheduling options
- Email queue prioritization
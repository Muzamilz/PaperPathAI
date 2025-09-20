"""
Email system disabled - No emails will be sent.
This module provides dummy functions when email is disabled.
"""
import logging

logger = logging.getLogger(__name__)


def send_request_confirmation_email_disabled(request_id, language='en'):
    """Dummy function - no email sent."""
    logger.info(f"Email disabled: Would send confirmation email for request {request_id} in {language}")
    return True


def send_status_update_email_disabled(request_id, old_status, new_status, language='en'):
    """Dummy function - no email sent."""
    logger.info(f"Email disabled: Would send status update email for request {request_id}: {old_status} -> {new_status}")
    return True


def send_admin_notification_email_disabled(request_id, notification_type='new_request'):
    """Dummy function - no email sent."""
    logger.info(f"Email disabled: Would send admin notification for request {request_id}: {notification_type}")
    return True
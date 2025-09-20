"""
Management command to test email notifications.
Usage: python manage.py test_email_notifications
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.service_requests.models import ServiceRequest
from apps.service_requests.tasks import (
    send_request_confirmation_email,
    send_status_update_email,
    send_admin_notification_email
)


class Command(BaseCommand):
    help = 'Test email notification system'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--request-id',
            type=int,
            help='ID of the service request to use for testing',
        )
        parser.add_argument(
            '--email-type',
            type=str,
            choices=['confirmation', 'status_update', 'admin_notification', 'all'],
            default='all',
            help='Type of email to test',
        )
        parser.add_argument(
            '--language',
            type=str,
            choices=['en', 'ar'],
            default='en',
            help='Language for the email template',
        )
    
    def handle(self, *args, **options):
        request_id = options.get('request_id')
        email_type = options.get('email_type')
        language = options.get('language')
        
        # Get a service request to test with
        if request_id:
            try:
                service_request = ServiceRequest.objects.get(id=request_id)
            except ServiceRequest.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Service request with ID {request_id} not found')
                )
                return
        else:
            # Get the most recent service request
            service_request = ServiceRequest.objects.first()
            if not service_request:
                self.stdout.write(
                    self.style.ERROR('No service requests found in the database')
                )
                return
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing emails for request: {service_request.project_title} (ID: {service_request.id})')
        )
        
        # Test confirmation email
        if email_type in ['confirmation', 'all']:
            self.stdout.write('Testing confirmation email...')
            try:
                result = send_request_confirmation_email.delay(service_request.id, language)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Confirmation email task queued: {result.id}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to queue confirmation email: {e}')
                )
        
        # Test status update email
        if email_type in ['status_update', 'all']:
            self.stdout.write('Testing status update email...')
            try:
                result = send_status_update_email.delay(
                    service_request.id, 
                    'pending', 
                    'in_progress', 
                    language
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Status update email task queued: {result.id}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to queue status update email: {e}')
                )
        
        # Test admin notification email
        if email_type in ['admin_notification', 'all']:
            self.stdout.write('Testing admin notification email...')
            
            # Check if there are admin users
            admin_count = User.objects.filter(is_staff=True, is_active=True).count()
            if admin_count == 0:
                self.stdout.write(
                    self.style.WARNING('No admin users found. Creating a test admin user...')
                )
                # Create a test admin user
                admin_user = User.objects.create_user(
                    username='testadmin',
                    email='admin@test.com',
                    password='testpass123',
                    is_staff=True,
                    is_active=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created test admin user: {admin_user.username}')
                )
            
            try:
                result = send_admin_notification_email.delay(service_request.id, 'new_request')
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Admin notification email task queued: {result.id}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to queue admin notification email: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nEmail testing completed! Check your email backend for the messages.')
        )
        self.stdout.write(
            'Note: If using console backend, check the Django server console output.'
        )
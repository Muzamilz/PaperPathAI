"""
Management command to send daily notifications.
This can be run as a cron job or scheduled task.
Usage: python manage.py send_daily_notifications
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.service_requests.models import ServiceRequest
from apps.service_requests.tasks import (
    send_daily_overdue_notifications,
    cleanup_old_attachments,
    send_admin_notification_email
)


class Command(BaseCommand):
    help = 'Send daily notifications and perform maintenance tasks'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually sending emails',
        )
        parser.add_argument(
            '--skip-overdue',
            action='store_true',
            help='Skip overdue notifications',
        )
        parser.add_argument(
            '--skip-cleanup',
            action='store_true',
            help='Skip attachment cleanup',
        )
    
    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        skip_overdue = options.get('skip_overdue', False)
        skip_cleanup = options.get('skip_cleanup', False)
        
        self.stdout.write(
            self.style.SUCCESS('Starting daily notifications and maintenance tasks...')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No emails will be sent')
            )
        
        # Send overdue notifications
        if not skip_overdue:
            self.stdout.write('Checking for overdue requests...')
            
            overdue_requests = ServiceRequest.objects.filter(
                deadline__lt=timezone.now().date(),
                status__in=['pending', 'in_progress']
            ).select_related('service')
            
            overdue_count = overdue_requests.count()
            self.stdout.write(f'Found {overdue_count} overdue requests')
            
            if overdue_count > 0 and not dry_run:
                try:
                    result = send_daily_overdue_notifications.delay()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Overdue notifications task queued: {result.id}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to queue overdue notifications: {e}')
                    )
            elif dry_run and overdue_count > 0:
                for request in overdue_requests:
                    self.stdout.write(
                        f'  - Would notify about: {request.project_title} (ID: {request.id})'
                    )
        
        # Check for high priority unassigned requests
        self.stdout.write('Checking for high priority unassigned requests...')
        
        high_priority_unassigned = ServiceRequest.objects.filter(
            priority__in=['high', 'urgent'],
            assigned_to=None,
            status='pending'
        ).select_related('service')
        
        unassigned_count = high_priority_unassigned.count()
        self.stdout.write(f'Found {unassigned_count} high priority unassigned requests')
        
        if unassigned_count > 0 and not dry_run:
            for request in high_priority_unassigned:
                try:
                    notification_type = 'urgent_request' if request.priority == 'urgent' else 'new_request'
                    send_admin_notification_email.delay(request.id, notification_type)
                    self.stdout.write(
                        f'✓ Queued notification for unassigned {request.priority} request: {request.project_title}'
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to queue notification for request {request.id}: {e}')
                    )
        elif dry_run and unassigned_count > 0:
            for request in high_priority_unassigned:
                self.stdout.write(
                    f'  - Would notify about unassigned {request.priority} request: {request.project_title}'
                )
        
        # Cleanup old attachments
        if not skip_cleanup:
            self.stdout.write('Checking for old attachments to cleanup...')
            
            cutoff_date = timezone.now() - timedelta(days=365)
            old_requests_with_attachments = ServiceRequest.objects.filter(
                created_at__lt=cutoff_date,
                status__in=['completed', 'cancelled'],
                attachments__isnull=False
            ).count()
            
            self.stdout.write(f'Found {old_requests_with_attachments} old requests with attachments')
            
            if old_requests_with_attachments > 0 and not dry_run:
                try:
                    result = cleanup_old_attachments.delay()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Cleanup task queued: {result.id}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to queue cleanup task: {e}')
                    )
        
        # Summary statistics
        self.stdout.write('\n' + '='*50)
        self.stdout.write('DAILY SUMMARY:')
        
        today = timezone.now().date()
        stats = {
            'new_today': ServiceRequest.objects.filter(created_at__date=today).count(),
            'pending': ServiceRequest.objects.filter(status='pending').count(),
            'in_progress': ServiceRequest.objects.filter(status='in_progress').count(),
            'completed_today': ServiceRequest.objects.filter(
                status='completed',
                updated_at__date=today
            ).count(),
            'overdue': len([r for r in ServiceRequest.objects.all() if r.is_overdue]),
            'unassigned': ServiceRequest.objects.filter(assigned_to=None, status='pending').count(),
        }
        
        self.stdout.write(f'New requests today: {stats["new_today"]}')
        self.stdout.write(f'Pending requests: {stats["pending"]}')
        self.stdout.write(f'In progress requests: {stats["in_progress"]}')
        self.stdout.write(f'Completed today: {stats["completed_today"]}')
        self.stdout.write(f'Overdue requests: {stats["overdue"]}')
        self.stdout.write(f'Unassigned requests: {stats["unassigned"]}')
        
        self.stdout.write(
            self.style.SUCCESS('\nDaily notifications and maintenance completed!')
        )
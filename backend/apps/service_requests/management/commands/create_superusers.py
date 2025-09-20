"""
Management command to create the required superusers.
Usage: python manage.py create_superusers
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create required superusers for the application'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating superusers...')
        
        # Create Ahmed admin user
        if not User.objects.filter(email='ahmed@admin.com').exists():
            User.objects.create_superuser(
                username='ahmed',
                email='ahmed@admin.com',
                password='735817677',
                first_name='Ahmed',
                last_name='Admin'
            )
            self.stdout.write(
                self.style.SUCCESS('✓ Ahmed superuser created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Ahmed superuser already exists')
            )
        
        # Create Muzamil admin user
        if not User.objects.filter(email='muzamil@admin.com').exists():
            User.objects.create_superuser(
                username='muzamil',
                email='muzamil@admin.com',
                password='muzamil2001117',
                first_name='Muzamil',
                last_name='Admin'
            )
            self.stdout.write(
                self.style.SUCCESS('✓ Muzamil superuser created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Muzamil superuser already exists')
            )
        
        # Remove default admin user if it exists
        if User.objects.filter(username='admin').exists():
            User.objects.filter(username='admin').delete()
            self.stdout.write(
                self.style.SUCCESS('✓ Default admin user removed')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Superuser setup completed!')
        )
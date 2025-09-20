"""
Custom admin site configuration for Student Services Website.
"""
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse


class StudentServicesAdminSite(admin.AdminSite):
    """Custom admin site with enhanced functionality."""
    
    site_header = 'PaperPath Administration'
    site_title = 'PaperPath Admin'
    index_title = 'Welcome to PaperPath Administration'
    
    def index(self, request, extra_context=None):
        """Custom admin index with dashboard links."""
        extra_context = extra_context or {}
        
        # Add custom dashboard links
        extra_context['dashboard_links'] = [
            {
                'title': 'Service Requests Dashboard',
                'url': reverse('admin:servicerequest_dashboard'),
                'description': 'View service request statistics and manage requests',
                'icon': '📊'
            },
            {
                'title': 'Overdue Requests',
                'url': reverse('admin:service_requests_servicerequest_changelist') + '?deadline__lt=' + 
                       str(__import__('django.utils.timezone', fromlist=['now']).now().date()),
                'description': 'View and manage overdue service requests',
                'icon': '⚠️'
            },
            {
                'title': 'Unassigned Requests',
                'url': reverse('admin:service_requests_servicerequest_changelist') + '?assigned_to__isnull=True',
                'description': 'View requests that need assignment',
                'icon': '📋'
            },
            {
                'title': 'Unread Inquiries',
                'url': reverse('admin:contact_contactinquiry_changelist') + '?is_read=False',
                'description': 'View unread contact inquiries',
                'icon': '✉️'
            }
        ]
        
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = StudentServicesAdminSite(name='student_services_admin')
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin interface for ServiceRequest with custom views for request management."""
    list_display = [
        'project_title', 'client_name', 'service', 'status', 'priority', 
        'deadline', 'is_overdue_display', 'assigned_to', 'created_at'
    ]
    list_filter = [
        'status', 'priority', 'service__category', 'assigned_to', 
        'created_at', 'deadline'
    ]
    search_fields = [
        'project_title', 'client_name', 'client_email', 
        'project_description', 'service__title'
    ]
    list_editable = ['status', 'priority', 'assigned_to']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Project Details', {
            'fields': ('service', 'project_title', 'project_description', 'deadline', 'budget')
        }),
        ('Request Management', {
            'fields': ('status', 'priority', 'assigned_to', 'notes')
        }),
        ('Attachments', {
            'fields': ('attachments',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'pending': 'orange',
            'in_progress': 'blue',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def priority_display(self, obj):
        """Display priority with color coding."""
        colors = {
            'low': 'green',
            'normal': 'blue',
            'high': 'orange',
            'urgent': 'red'
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_display.short_description = 'Priority'
    
    def is_overdue_display(self, obj):
        """Display overdue status with color coding."""
        if obj.is_overdue:
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠ Overdue</span>'
            )
        return format_html(
            '<span style="color: green;">✓ On Time</span>'
        )
    is_overdue_display.short_description = 'Deadline Status'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'service', 'service__category', 'assigned_to'
        )
    
    actions = [
        'mark_as_in_progress', 'mark_as_completed', 'mark_as_cancelled',
        'assign_to_me', 'set_high_priority', 'set_normal_priority'
    ]
    
    def mark_as_in_progress(self, request, queryset):
        """Bulk action to mark requests as in progress."""
        updated = queryset.update(status='in_progress')
        self.message_user(
            request, 
            f'{updated} request(s) marked as in progress.'
        )
    mark_as_in_progress.short_description = 'Mark selected requests as in progress'
    
    def mark_as_completed(self, request, queryset):
        """Bulk action to mark requests as completed."""
        updated = queryset.update(status='completed')
        self.message_user(
            request, 
            f'{updated} request(s) marked as completed.'
        )
    mark_as_completed.short_description = 'Mark selected requests as completed'
    
    def mark_as_cancelled(self, request, queryset):
        """Bulk action to mark requests as cancelled."""
        updated = queryset.update(status='cancelled')
        self.message_user(
            request, 
            f'{updated} request(s) marked as cancelled.'
        )
    mark_as_cancelled.short_description = 'Mark selected requests as cancelled'
    
    def assign_to_me(self, request, queryset):
        """Bulk action to assign requests to current user."""
        updated = queryset.update(assigned_to=request.user)
        self.message_user(
            request, 
            f'{updated} request(s) assigned to you.'
        )
    assign_to_me.short_description = 'Assign selected requests to me'
    
    def set_high_priority(self, request, queryset):
        """Bulk action to set requests to high priority."""
        updated = queryset.update(priority='high')
        self.message_user(
            request, 
            f'{updated} request(s) set to high priority.'
        )
    set_high_priority.short_description = 'Set selected requests to high priority'
    
    def set_normal_priority(self, request, queryset):
        """Bulk action to set requests to normal priority."""
        updated = queryset.update(priority='normal')
        self.message_user(
            request, 
            f'{updated} request(s) set to normal priority.'
        )
    set_normal_priority.short_description = 'Set selected requests to normal priority'
    
    def get_urls(self):
        """Add custom URLs for dashboard views."""
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='servicerequest_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view for request management."""
        # Get statistics
        total_requests = ServiceRequest.objects.count()
        pending_requests = ServiceRequest.objects.filter(status='pending').count()
        in_progress_requests = ServiceRequest.objects.filter(status='in_progress').count()
        completed_requests = ServiceRequest.objects.filter(status='completed').count()
        overdue_requests = ServiceRequest.objects.filter(
            deadline__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        ).count()
        
        # Get requests by priority
        priority_stats = ServiceRequest.objects.values('priority').annotate(
            count=Count('id')
        ).order_by('priority')
        
        # Get recent requests
        recent_requests = ServiceRequest.objects.select_related(
            'service', 'service__category', 'assigned_to'
        ).order_by('-created_at')[:10]
        
        # Get overdue requests
        overdue_requests_list = ServiceRequest.objects.filter(
            deadline__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        ).select_related('service', 'assigned_to').order_by('deadline')[:10]
        
        context = {
            'title': 'Service Requests Dashboard',
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'in_progress_requests': in_progress_requests,
            'completed_requests': completed_requests,
            'overdue_requests': overdue_requests,
            'priority_stats': priority_stats,
            'recent_requests': recent_requests,
            'overdue_requests_list': overdue_requests_list,
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/service_requests/dashboard.html', context)
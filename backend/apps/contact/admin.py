from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(TranslationAdmin):
    """Admin interface for ContactInquiry with response tracking and translation support."""
    list_display = [
        'subject', 'name', 'email', 'inquiry_type', 
        'is_read', 'is_responded', 'created_at'
    ]
    list_filter = [
        'inquiry_type', 'is_read', 'is_responded', 'created_at'
    ]
    search_fields = [
        'name', 'email', 'subject', 'message', 'response_notes',
        'subject_en', 'subject_ar', 'message_en', 'message_ar'
    ]
    list_editable = ['is_read', 'is_responded']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Response Management', {
            'fields': ('is_read', 'is_responded', 'response_notes')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # Translation-specific settings
    group_fieldsets = True
    
    def is_read_display(self, obj):
        """Display read status with color coding."""
        if obj.is_read:
            return format_html(
                '<span style="color: green;">✓ Read</span>'
            )
        return format_html(
            '<span style="color: orange; font-weight: bold;">✗ Unread</span>'
        )
    is_read_display.short_description = 'Read'
    
    def is_responded_display(self, obj):
        """Display response status with color coding."""
        if obj.is_responded:
            return format_html(
                '<span style="color: green;">✓ Responded</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Pending</span>'
        )
    is_responded_display.short_description = 'Response'
    
    actions = ['mark_as_read', 'mark_as_responded', 'mark_as_unread', 'mark_as_not_responded']
    
    def mark_as_read(self, request, queryset):
        """Bulk action to mark inquiries as read."""
        updated = queryset.update(is_read=True)
        self.message_user(
            request, 
            f'{updated} inquiry(ies) marked as read.'
        )
    mark_as_read.short_description = 'Mark selected inquiries as read'
    
    def mark_as_responded(self, request, queryset):
        """Bulk action to mark inquiries as responded."""
        updated = queryset.update(is_responded=True)
        self.message_user(
            request, 
            f'{updated} inquiry(ies) marked as responded.'
        )
    mark_as_responded.short_description = 'Mark selected inquiries as responded'
    
    def mark_as_unread(self, request, queryset):
        """Bulk action to mark inquiries as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(
            request, 
            f'{updated} inquiry(ies) marked as unread.'
        )
    mark_as_unread.short_description = 'Mark selected inquiries as unread'
    
    def mark_as_not_responded(self, request, queryset):
        """Bulk action to mark inquiries as not responded."""
        updated = queryset.update(is_responded=False)
        self.message_user(
            request, 
            f'{updated} inquiry(ies) marked as not responded.'
        )
    mark_as_not_responded.short_description = 'Mark selected inquiries as not responded'
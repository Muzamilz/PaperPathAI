from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from .models import PortfolioItem


@admin.register(PortfolioItem)
class PortfolioItemAdmin(TranslationAdmin):
    """Admin interface for PortfolioItem with translation support."""
    list_display = [
        'title', 'service_category', 'client_type', 'completion_date', 
        'is_featured', 'is_active', 'image_preview', 'order'
    ]
    list_filter = [
        'is_featured', 'is_active', 'service_category', 
        'completion_date', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'client_type', 'technologies_used',
        'title_en', 'title_ar', 'description_en', 'description_ar'
    ]
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['-is_featured', 'order', '-completion_date']
    date_hierarchy = 'completion_date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'service_category')
        }),
        ('Project Details', {
            'fields': ('client_type', 'completion_date', 'project_duration', 'technologies_used')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    # Translation-specific settings
    group_fieldsets = True
    
    def image_preview(self, obj):
        """Display image preview in admin list."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('service_category')
    
    actions = ['mark_as_featured', 'unmark_as_featured']
    
    def mark_as_featured(self, request, queryset):
        """Bulk action to mark items as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request, 
            f'{updated} portfolio item(s) marked as featured.'
        )
    mark_as_featured.short_description = 'Mark selected items as featured'
    
    def unmark_as_featured(self, request, queryset):
        """Bulk action to unmark items as featured."""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request, 
            f'{updated} portfolio item(s) unmarked as featured.'
        )
    unmark_as_featured.short_description = 'Unmark selected items as featured'
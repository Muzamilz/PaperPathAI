from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(TranslationAdmin):
    """Admin interface for ServiceCategory with translation support."""
    list_display = ['name', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description', 'name_en', 'name_ar', 'description_en', 'description_ar']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'slug', 'parent')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    # Translation-specific settings
    group_fieldsets = True


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    """Admin interface for Service with translation support."""
    list_display = ['title', 'category', 'price_range', 'delivery_time', 'is_active', 'order']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = [
        'title', 'description', 'short_description',
        'title_en', 'title_ar', 'description_en', 'description_ar',
        'short_description_en', 'short_description_ar'
    ]
    list_editable = ['is_active', 'order']
    ordering = ['category', 'order', 'title']
    
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'description', 'short_description')
        }),
        ('Service Details', {
            'fields': ('price_range', 'delivery_time', 'features')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    # Translation-specific settings
    group_fieldsets = True
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('category')
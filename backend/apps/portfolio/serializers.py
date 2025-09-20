"""
Serializers for portfolio app.
"""
from rest_framework import serializers
from .models import PortfolioItem
from apps.services.serializers import ServiceCategorySerializer


class PortfolioItemSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioItem model with translation support and image handling."""
    service_category_name = serializers.ReadOnlyField(source='service_category.name')
    service_category_slug = serializers.ReadOnlyField(source='service_category.slug')
    image_url = serializers.SerializerMethodField()
    
    # Translation fields
    title_en = serializers.CharField(read_only=True)
    title_ar = serializers.CharField(read_only=True)
    description_en = serializers.CharField(read_only=True)
    description_ar = serializers.CharField(read_only=True)
    technologies_used_en = serializers.JSONField(read_only=True)
    technologies_used_ar = serializers.JSONField(read_only=True)
    
    class Meta:
        model = PortfolioItem
        fields = [
            'id', 'title', 'description', 'service_category', 'service_category_name',
            'service_category_slug', 'image', 'image_url', 'client_type', 'completion_date', 
            'technologies_used', 'project_duration', 'is_featured', 'is_active', 'order',
            'created_at', 'updated_at', 'title_en', 'title_ar', 'description_en', 
            'description_ar', 'technologies_used_en', 'technologies_used_ar'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Get full URL for image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_title(self, value):
        """Validate portfolio title."""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()
    
    def validate_description(self, value):
        """Validate portfolio description."""
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value.strip()
    
    def validate_technologies_used(self, value):
        """Validate technologies used field."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Technologies used must be a list.")
        return value
    
    def validate_image(self, value):
        """Validate image file."""
        if value:
            # Check file size (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size cannot exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Invalid image format. Allowed formats: JPEG, PNG, WebP"
                )
        
        return value
    
    def validate_completion_date(self, value):
        """Validate completion date is not in the future."""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Completion date cannot be in the future.")
        return value


class PortfolioItemAdminSerializer(PortfolioItemSerializer):
    """Admin serializer for PortfolioItem with additional fields."""
    service_category = ServiceCategorySerializer(read_only=True)
    
    class Meta(PortfolioItemSerializer.Meta):
        fields = PortfolioItemSerializer.Meta.fields
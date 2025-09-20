"""
Serializers for services app.
"""
from rest_framework import serializers
from django.conf import settings
from .models import ServiceCategory, Service


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for ServiceCategory model with translation support."""
    children = serializers.SerializerMethodField()
    full_path = serializers.ReadOnlyField(source='get_full_path')
    
    # Translation fields
    name_en = serializers.CharField(read_only=True)
    name_ar = serializers.CharField(read_only=True)
    description_en = serializers.CharField(read_only=True)
    description_ar = serializers.CharField(read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name', 'description', 'slug', 'parent', 'children',
            'full_path', 'is_active', 'order', 'created_at', 'updated_at',
            'name_en', 'name_ar', 'description_en', 'description_ar'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_children(self, obj):
        """Get child categories."""
        children = obj.children.filter(is_active=True).order_by('order', 'name')
        return ServiceCategorySerializer(children, many=True, context=self.context).data
    
    def validate(self, data):
        """Validate category data."""
        # Prevent circular parent relationships
        if 'parent' in data and data['parent']:
            parent = data['parent']
            if parent == self.instance:
                raise serializers.ValidationError("A category cannot be its own parent.")
            
            # Check for circular reference
            current_parent = parent.parent
            while current_parent:
                if current_parent == self.instance:
                    raise serializers.ValidationError("Circular parent relationship detected.")
                current_parent = current_parent.parent
        
        return data


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model with translation support."""
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')
    
    # Translation fields
    title_en = serializers.CharField(read_only=True)
    title_ar = serializers.CharField(read_only=True)
    description_en = serializers.CharField(read_only=True)
    description_ar = serializers.CharField(read_only=True)
    short_description_en = serializers.CharField(read_only=True)
    short_description_ar = serializers.CharField(read_only=True)
    features_en = serializers.JSONField(read_only=True)
    features_ar = serializers.JSONField(read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'category', 'category_name', 'category_slug', 'title', 'description', 
            'short_description', 'price_range', 'delivery_time', 'features',
            'is_active', 'order', 'created_at', 'updated_at',
            'title_en', 'title_ar', 'description_en', 'description_ar',
            'short_description_en', 'short_description_ar', 'features_en', 'features_ar'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_features(self, value):
        """Validate features field."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Features must be a list.")
        return value
    
    def validate_price_range(self, value):
        """Validate price range format."""
        if not value.strip():
            raise serializers.ValidationError("Price range cannot be empty.")
        return value.strip()
    
    def validate_delivery_time(self, value):
        """Validate delivery time format."""
        if not value.strip():
            raise serializers.ValidationError("Delivery time cannot be empty.")
        return value.strip()


class ServiceCategoryAdminSerializer(ServiceCategorySerializer):
    """Admin serializer for ServiceCategory with additional fields."""
    services_count = serializers.SerializerMethodField()
    
    class Meta(ServiceCategorySerializer.Meta):
        fields = ServiceCategorySerializer.Meta.fields + ['services_count']
    
    def get_services_count(self, obj):
        """Get count of services in this category."""
        return obj.services.count()


class ServiceAdminSerializer(ServiceSerializer):
    """Admin serializer for Service with additional fields."""
    requests_count = serializers.SerializerMethodField()
    
    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields + ['requests_count']
    
    def get_requests_count(self, obj):
        """Get count of requests for this service."""
        return obj.requests.count()
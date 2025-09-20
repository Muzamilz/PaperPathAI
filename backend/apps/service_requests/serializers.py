"""
Serializers for service_requests app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ServiceRequest
from apps.services.serializers import ServiceSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ServiceRequestSerializer(serializers.ModelSerializer):
    """Serializer for ServiceRequest model with comprehensive validation."""
    service_title = serializers.ReadOnlyField(source='service.title')
    service_category = serializers.ReadOnlyField(source='service.category.name')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.get_full_name')
    is_overdue = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField(source='get_status_display')
    priority_display = serializers.ReadOnlyField(source='get_priority_display')
    
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'service', 'service_title', 'service_category', 'client_name', 'client_email', 
            'client_phone', 'project_title', 'project_description', 'deadline',
            'budget', 'status', 'status_display', 'priority', 'priority_display',
            'assigned_to', 'assigned_to_name', 'notes', 'attachments',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_client_name(self, value):
        """Validate client name."""
        if not value.strip():
            raise serializers.ValidationError("Client name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Client name must be at least 2 characters long.")
        return value.strip()
    
    def validate_client_email(self, value):
        """Validate client email."""
        if not value.strip():
            raise serializers.ValidationError("Client email cannot be empty.")
        return value.lower().strip()
    
    def validate_project_title(self, value):
        """Validate project title."""
        if not value.strip():
            raise serializers.ValidationError("Project title cannot be empty.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Project title must be at least 5 characters long.")
        return value.strip()
    
    def validate_project_description(self, value):
        """Validate project description."""
        if not value.strip():
            raise serializers.ValidationError("Project description cannot be empty.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Project description must be at least 20 characters long.")
        return value.strip()
    
    def validate_deadline(self, value):
        """Validate deadline is in the future."""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value
    
    def validate_budget(self, value):
        """Validate budget format."""
        if not value.strip():
            raise serializers.ValidationError("Budget cannot be empty.")
        return value.strip()
    
    def validate_attachments(self, value):
        """Validate attachment file size and type."""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB.")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
            file_extension = value.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        
        return value


class ServiceRequestPublicSerializer(serializers.ModelSerializer):
    """Public serializer for ServiceRequest submissions (excludes admin fields)."""
    service_title = serializers.ReadOnlyField(source='service.title')
    service_category = serializers.ReadOnlyField(source='service.category.name')
    
    class Meta:
        model = ServiceRequest
        fields = [
            'service', 'service_title', 'service_category', 'client_name', 'client_email', 
            'client_phone', 'project_title', 'project_description', 'deadline',
            'budget', 'attachments'
        ]
    
    def validate_client_name(self, value):
        """Validate client name."""
        if not value.strip():
            raise serializers.ValidationError("Client name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Client name must be at least 2 characters long.")
        return value.strip()
    
    def validate_client_email(self, value):
        """Validate client email."""
        if not value.strip():
            raise serializers.ValidationError("Client email cannot be empty.")
        return value.lower().strip()
    
    def validate_project_title(self, value):
        """Validate project title."""
        if not value.strip():
            raise serializers.ValidationError("Project title cannot be empty.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Project title must be at least 5 characters long.")
        return value.strip()
    
    def validate_project_description(self, value):
        """Validate project description."""
        if not value.strip():
            raise serializers.ValidationError("Project description cannot be empty.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Project description must be at least 20 characters long.")
        return value.strip()
    
    def validate_deadline(self, value):
        """Validate deadline is in the future."""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value
    
    def validate_budget(self, value):
        """Validate budget format."""
        if not value.strip():
            raise serializers.ValidationError("Budget cannot be empty.")
        return value.strip()
    
    def validate_attachments(self, value):
        """Validate attachment file size and type."""
        if value:
            # Check file size (max 10MB)
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 10MB.")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
            file_extension = value.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        
        return value


class ServiceRequestAdminSerializer(ServiceRequestSerializer):
    """Admin serializer for ServiceRequest with additional fields."""
    service = ServiceSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    
    class Meta(ServiceRequestSerializer.Meta):
        fields = ServiceRequestSerializer.Meta.fields
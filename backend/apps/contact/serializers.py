"""
Serializers for contact app.
"""
from rest_framework import serializers
from .models import ContactInquiry
import re


class ContactInquirySerializer(serializers.ModelSerializer):
    """Serializer for ContactInquiry model with comprehensive validation."""
    inquiry_type_display = serializers.ReadOnlyField(source='get_inquiry_type_display')
    
    class Meta:
        model = ContactInquiry
        fields = [
            'id', 'name', 'email', 'phone', 'inquiry_type', 'inquiry_type_display',
            'subject', 'message', 'is_read', 'is_responded', 'response_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_read', 'is_responded', 'response_notes']
    
    def validate_name(self, value):
        """Validate contact name."""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Name cannot exceed 100 characters.")
        return value.strip()
    
    def validate_email(self, value):
        """Validate email format."""
        if not value.strip():
            raise serializers.ValidationError("Email cannot be empty.")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value.strip()):
            raise serializers.ValidationError("Please enter a valid email address.")
        
        return value.lower().strip()
    
    def validate_phone(self, value):
        """Validate phone number format."""
        if value and value.strip():
            # Remove spaces and common separators
            cleaned_phone = re.sub(r'[\s\-\(\)]+', '', value.strip())
            
            # Check if it contains only digits and + (for international)
            if not re.match(r'^\+?[0-9]{8,15}$', cleaned_phone):
                raise serializers.ValidationError(
                    "Please enter a valid phone number (8-15 digits, optionally starting with +)."
                )
            
            return value.strip()
        return value
    
    def validate_subject(self, value):
        """Validate subject."""
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Subject must be at least 5 characters long.")
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Subject cannot exceed 200 characters.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message."""
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        if len(value.strip()) > 2000:
            raise serializers.ValidationError("Message cannot exceed 2000 characters.")
        return value.strip()


class ContactInquiryPublicSerializer(serializers.ModelSerializer):
    """Public serializer for ContactInquiry submissions (excludes admin fields)."""
    
    class Meta:
        model = ContactInquiry
        fields = [
            'name', 'email', 'phone', 'inquiry_type', 'subject', 'message'
        ]
    
    def validate_name(self, value):
        """Validate contact name."""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Name cannot exceed 100 characters.")
        return value.strip()
    
    def validate_email(self, value):
        """Validate email format."""
        if not value.strip():
            raise serializers.ValidationError("Email cannot be empty.")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value.strip()):
            raise serializers.ValidationError("Please enter a valid email address.")
        
        return value.lower().strip()
    
    def validate_phone(self, value):
        """Validate phone number format."""
        if value and value.strip():
            # Remove spaces and common separators
            cleaned_phone = re.sub(r'[\s\-\(\)]+', '', value.strip())
            
            # Check if it contains only digits and + (for international)
            if not re.match(r'^\+?[0-9]{8,15}$', cleaned_phone):
                raise serializers.ValidationError(
                    "Please enter a valid phone number (8-15 digits, optionally starting with +)."
                )
            
            return value.strip()
        return value
    
    def validate_subject(self, value):
        """Validate subject."""
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Subject must be at least 5 characters long.")
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Subject cannot exceed 200 characters.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message."""
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        if len(value.strip()) > 2000:
            raise serializers.ValidationError("Message cannot exceed 2000 characters.")
        return value.strip()


class ContactInquiryAdminSerializer(ContactInquirySerializer):
    """Admin serializer for ContactInquiry with additional fields."""
    
    class Meta(ContactInquirySerializer.Meta):
        fields = ContactInquirySerializer.Meta.fields
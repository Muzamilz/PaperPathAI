from django.db import models


class ContactInquiry(models.Model):
    """Model for contact form submissions."""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('service', 'Service Question'),
        ('quote', 'Quote Request'),
        ('support', 'Support'),
        ('partnership', 'Partnership'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    response_notes = models.TextField(blank=True, help_text="Internal notes about response")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name} ({self.get_inquiry_type_display()})"
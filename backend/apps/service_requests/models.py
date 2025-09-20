from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Service


class ServiceRequest(models.Model):
    """Model for service requests with status tracking."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    deadline = models.DateField()
    budget = models.CharField(max_length=100, help_text="Client's budget range")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    notes = models.TextField(blank=True, help_text="Internal notes for staff")
    attachments = models.FileField(upload_to='request_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_title} - {self.client_name} ({self.get_status_display()})"

    @property
    def is_overdue(self):
        """Check if the request is overdue based on deadline."""
        from django.utils import timezone
        return self.deadline < timezone.now().date() and self.status not in ['completed', 'cancelled']
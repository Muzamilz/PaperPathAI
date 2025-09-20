from django.db import models
from apps.services.models import ServiceCategory


class PortfolioItem(models.Model):
    """Model for portfolio items with translation support."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='portfolio_items')
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    client_type = models.CharField(max_length=100, help_text="Anonymized client type (e.g., 'University Student', 'Graduate Researcher')")
    completion_date = models.DateField()
    technologies_used = models.JSONField(default=list, help_text="List of technologies or tools used")
    project_duration = models.CharField(max_length=50, blank=True, help_text="e.g., '2 weeks', '1 month'")
    is_featured = models.BooleanField(default=False, help_text="Display in featured portfolio section")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Portfolio Item'
        verbose_name_plural = 'Portfolio Items'
        ordering = ['-is_featured', 'order', '-completion_date']

    def __str__(self):
        return f"{self.title} ({self.service_category.name})"
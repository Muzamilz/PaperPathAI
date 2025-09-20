from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """Model for service categories with hierarchical structure and translation support."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_full_path(self):
        """Return the full path of the category including parent categories."""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Service(models.Model):
    """Model for individual services with multilingual support."""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    price_range = models.CharField(max_length=100, help_text="e.g., '$50-100', 'Starting from $25'")
    delivery_time = models.CharField(max_length=100, help_text="e.g., '3-5 days', '1 week'")
    features = models.JSONField(default=list, help_text="List of service features")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['category', 'order', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.name})"
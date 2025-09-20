"""
Translation configuration for services app models.
"""
from modeltranslation.translator import register, TranslationOptions
from .models import ServiceCategory, Service


@register(ServiceCategory)
class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'short_description', 'features')
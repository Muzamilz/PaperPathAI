"""
Translation configuration for portfolio app models.
"""
from modeltranslation.translator import register, TranslationOptions
from .models import PortfolioItem


@register(PortfolioItem)
class PortfolioItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'technologies_used')
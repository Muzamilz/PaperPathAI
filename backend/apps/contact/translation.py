"""
Translation configuration for contact app models.
"""
from modeltranslation.translator import register, TranslationOptions
from .models import ContactInquiry


@register(ContactInquiry)
class ContactInquiryTranslationOptions(TranslationOptions):
    fields = ('subject', 'message', 'response_notes')
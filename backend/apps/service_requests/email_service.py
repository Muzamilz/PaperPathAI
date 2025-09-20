"""
Email service for service requests with multilingual support.
This module provides a centralized way to manage email templates and notifications.
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json


class EmailTemplateService:
    """Service class for managing email templates and sending notifications."""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@studentservices.com')
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    
    def get_email_templates(self):
        """
        Get all email templates with multilingual support.
        This centralizes all email content and makes it easy to maintain.
        """
        return {
            'request_confirmation': {
                'en': {
                    'subject': 'Service Request Confirmation - {project_title}',
                    'greeting': 'Dear {client_name},',
                    'body': '''Thank you for submitting your service request. We have received your request and will review it shortly.

<strong>Request Details:</strong>
• Service: {service_name}
• Project: {project_title}
• Request ID: #{request_id}
• Submitted: {created_at}
• Deadline: {deadline}

<strong>What happens next?</strong>
1. Our team will review your request within 24 hours
2. We will contact you to discuss project requirements
3. You will receive a detailed quote and timeline
4. Upon approval, we will begin working on your project

You can track your request status by visiting: {tracking_url}

If you have any questions, please don't hesitate to contact us at {contact_email} or call {contact_phone}.''',
                    'footer': 'Best regards,<br>Student Services Team<br><br><small>This is an automated message. Please do not reply to this email.</small>',
                    'contact_email': 'support@studentservices.com',
                    'contact_phone': '+1 (555) 123-4567'
                },
                'ar': {
                    'subject': 'تأكيد طلب الخدمة - {project_title}',
                    'greeting': 'عزيزي {client_name}،',
                    'body': '''شكراً لك على تقديم طلب الخدمة. لقد استلمنا طلبك وسنقوم بمراجعته قريباً.

<strong>تفاصيل الطلب:</strong>
• الخدمة: {service_name}
• المشروع: {project_title}
• رقم الطلب: #{request_id}
• تاريخ التقديم: {created_at}
• الموعد النهائي: {deadline}

<strong>الخطوات التالية:</strong>
1. سيقوم فريقنا بمراجعة طلبك خلال 24 ساعة
2. سنتواصل معك لمناقشة متطلبات المشروع
3. ستحصل على عرض سعر مفصل وجدول زمني
4. بعد الموافقة، سنبدأ العمل على مشروعك

يمكنك تتبع حالة طلبك من خلال زيارة: {tracking_url}

إذا كان لديك أي استفسارات، لا تتردد في التواصل معنا على {contact_email} أو الاتصال على {contact_phone}.''',
                    'footer': 'مع أطيب التحيات،<br>فريق خدمات الطلاب<br><br><small>هذه رسالة تلقائية. يرجى عدم الرد على هذا البريد الإلكتروني.</small>',
                    'contact_email': 'support@studentservices.com',
                    'contact_phone': '+1 (555) 123-4567'
                }
            },
            'status_update': {
                'en': {
                    'subject': 'Service Request Update - {project_title}',
                    'greeting': 'Dear {client_name},',
                    'body': '''Your service request status has been updated.

<strong>Request Details:</strong>
• Service: {service_name}
• Project: {project_title}
• Request ID: #{request_id}
• Previous Status: {old_status}
• New Status: <strong>{new_status}</strong>

{status_message}

You can view the full details of your request here: {tracking_url}

If you have any questions about this update, please contact us at {contact_email}.''',
                    'footer': 'Best regards,<br>Student Services Team<br><br><small>This is an automated message. Please do not reply to this email.</small>',
                    'contact_email': 'support@studentservices.com'
                },
                'ar': {
                    'subject': 'تحديث طلب الخدمة - {project_title}',
                    'greeting': 'عزيزي {client_name}،',
                    'body': '''تم تحديث حالة طلب الخدمة الخاص بك.

<strong>تفاصيل الطلب:</strong>
• الخدمة: {service_name}
• المشروع: {project_title}
• رقم الطلب: #{request_id}
• الحالة السابقة: {old_status}
• الحالة الجديدة: <strong>{new_status}</strong>

{status_message}

يمكنك عرض التفاصيل الكاملة لطلبك هنا: {tracking_url}

إذا كان لديك أي استفسارات حول هذا التحديث، يرجى التواصل معنا على {contact_email}.''',
                    'footer': 'مع أطيب التحيات،<br>فريق خدمات الطلاب<br><br><small>هذه رسالة تلقائية. يرجى عدم الرد على هذا البريد الإلكتروني.</small>',
                    'contact_email': 'support@studentservices.com'
                }
            },
            'admin_notification': {
                'en': {
                    'subject': 'New Service Request: {project_title}',
                    'greeting': 'Hello Admin,',
                    'body': '''A new service request has been submitted and requires attention.

<strong>Request Details:</strong>
• Client: {client_name} ({client_email})
• Phone: {client_phone}
• Service: {service_name}
• Project: {project_title}
• Priority: <strong>{priority}</strong>
• Deadline: {deadline}
• Budget: {budget}
• Request ID: #{request_id}
• Submitted: {created_at}

<strong>Project Description:</strong>
{project_description}

Please review this request in the admin dashboard: {admin_url}

{urgency_note}''',
                    'footer': 'Student Services Admin System',
                    'urgency_high': '<strong>⚠️ HIGH PRIORITY REQUEST</strong> - This request has been marked as high priority and requires immediate attention.',
                    'urgency_urgent': '<strong>🚨 URGENT REQUEST</strong> - This request is marked as URGENT and needs immediate action.',
                    'urgency_overdue': '<strong>⏰ OVERDUE ALERT</strong> - This request is past its deadline and requires immediate attention.'
                }
            }
        }
    
    def get_status_messages(self):
        """Get status-specific messages for different languages."""
        return {
            'en': {
                'in_progress': '''<strong>Great news!</strong> We have started working on your project. Our team will keep you updated on the progress.

<strong>What to expect:</strong>
• Regular progress updates
• Direct communication with your assigned team member
• Quality assurance checks throughout the process''',
                'completed': '''<strong>Excellent!</strong> Your project has been completed successfully.

<strong>Next steps:</strong>
• Check your email for the deliverables
• Review the completed work
• Provide feedback if needed
• Request revisions if necessary (within the agreed terms)''',
                'cancelled': '''Your service request has been cancelled.

If this cancellation was unexpected or if you have any questions, please contact us immediately at {contact_email}.

We apologize for any inconvenience and would be happy to discuss alternative solutions.''',
            },
            'ar': {
                'in_progress': '''<strong>أخبار رائعة!</strong> لقد بدأنا العمل على مشروعك. سيقوم فريقنا بإبقائك على اطلاع بالتقدم.

<strong>ما يمكن توقعه:</strong>
• تحديثات منتظمة حول التقدم
• تواصل مباشر مع عضو الفريق المخصص لك
• فحوصات ضمان الجودة طوال العملية''',
                'completed': '''<strong>ممتاز!</strong> تم إنجاز مشروعك بنجاح.

<strong>الخطوات التالية:</strong>
• تحقق من بريدك الإلكتروني للحصول على المخرجات
• راجع العمل المنجز
• قدم ملاحظاتك إذا لزم الأمر
• اطلب تعديلات إذا لزم الأمر (ضمن الشروط المتفق عليها)''',
                'cancelled': '''تم إلغاء طلب الخدمة الخاص بك.

إذا كان هذا الإلغاء غير متوقع أو إذا كان لديك أي استفسارات، يرجى التواصل معنا فوراً على {contact_email}.

نعتذر عن أي إزعاج ونسعد بمناقشة حلول بديلة.''',
            }
        }
    
    def create_html_email(self, template_content, context):
        """Create HTML email content from template."""
        html_template = f'''
<!DOCTYPE html>
<html dir="{context.get('direction', 'ltr')}" lang="{context.get('language', 'en')}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template_content['subject']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .email-container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 24px;
            font-weight: bold;
            color: #3b82f6;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .footer {{
            border-top: 1px solid #e5e7eb;
            padding-top: 20px;
            margin-top: 30px;
            color: #6b7280;
            font-size: 14px;
        }}
        .button {{
            display: inline-block;
            background-color: #3b82f6;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin: 15px 0;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-pending {{ background-color: #fef3c7; color: #92400e; }}
        .status-in_progress {{ background-color: #dbeafe; color: #1e40af; }}
        .status-completed {{ background-color: #d1fae5; color: #065f46; }}
        .status-cancelled {{ background-color: #fee2e2; color: #991b1b; }}
        .priority-high {{ color: #dc2626; font-weight: bold; }}
        .priority-urgent {{ color: #dc2626; font-weight: bold; background-color: #fee2e2; padding: 2px 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="logo">Student Services</div>
        </div>
        <div class="content">
            <p>{template_content['greeting']}</p>
            <div>{template_content['body']}</div>
        </div>
        <div class="footer">
            {template_content['footer']}
        </div>
    </div>
</body>
</html>
        '''
        
        # Format the HTML template with context
        try:
            return html_template.format(**context)
        except KeyError as e:
            # If formatting fails, return a simple version
            return f"<html><body><p>{template_content['greeting']}</p><div>{template_content['body']}</div><p>{template_content['footer']}</p></body></html>"
    
    def send_email(self, template_type, language, context, recipient_list, notification_type=None):
        """
        Send email using the specified template and context.
        
        Args:
            template_type (str): Type of email template
            language (str): Language code ('en' or 'ar')
            context (dict): Context variables for template
            recipient_list (list): List of recipient email addresses
            notification_type (str): Optional notification type for admin emails
        """
        templates = self.get_email_templates()
        status_messages = self.get_status_messages()
        
        # Get the template
        template = templates.get(template_type, {}).get(language)
        if not template:
            template = templates.get(template_type, {}).get('en', {})
        
        if not template:
            raise ValueError(f"Template not found: {template_type}")
        
        # Add default context values
        context.update({
            'language': language,
            'direction': 'rtl' if language == 'ar' else 'ltr',
            'tracking_url': f"{self.frontend_url}/track/{context.get('request_id', '')}",
            'admin_url': f"{self.frontend_url}/admin/requests/{context.get('request_id', '')}",
            'contact_email': template.get('contact_email', 'support@studentservices.com'),
            'contact_phone': template.get('contact_phone', '+1 (555) 123-4567'),
        })
        
        # Add status-specific messages
        if template_type == 'status_update' and 'new_status' in context:
            status_msg = status_messages.get(language, status_messages['en']).get(context['new_status'], '')
            context['status_message'] = status_msg.format(**context)
        
        # Add urgency notes for admin notifications
        if template_type == 'admin_notification' and notification_type:
            urgency_key = f'urgency_{notification_type.replace("_request", "").replace("_", "")}'
            context['urgency_note'] = template.get(urgency_key, '')
        else:
            context['urgency_note'] = ''
        
        # Format template content
        formatted_template = {}
        for key, value in template.items():
            try:
                formatted_template[key] = value.format(**context)
            except (KeyError, ValueError):
                formatted_template[key] = value
        
        # Create HTML and plain text versions
        html_content = self.create_html_email(formatted_template, context)
        plain_content = strip_tags(html_content).replace('<br>', '\n')
        
        # Send email
        email = EmailMultiAlternatives(
            subject=formatted_template['subject'],
            body=plain_content,
            from_email=self.from_email,
            to=recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        
        return email.send()


# Global instance
email_service = EmailTemplateService()
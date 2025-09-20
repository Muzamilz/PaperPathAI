"""
Dashboard API views for aggregated data.
"""
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.services.models import ServiceCategory, Service
from apps.service_requests.models import ServiceRequest
from apps.portfolio.models import PortfolioItem
from apps.contact.models import ContactInquiry


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_stats(request):
    """Get basic dashboard statistics for admin panel."""
    # Basic stats
    stats = {
        'totalServices': Service.objects.filter(is_active=True).count(),
        'pendingRequests': ServiceRequest.objects.filter(status='pending').count(),
        'activeRequests': ServiceRequest.objects.filter(status='in_progress').count(),
        'portfolioItems': PortfolioItem.objects.filter(is_active=True).count(),
    }
    
    # Recent activity (simplified for frontend)
    recent_requests = ServiceRequest.objects.select_related('service').order_by('-created_at')[:5]
    recent_activity = []
    
    for request in recent_requests:
        recent_activity.append({
            'id': request.id,
            'type': 'request',
            'description': f'New service request: {request.project_title}',
            'created_at': request.created_at.isoformat(),
        })
    
    return Response({
        'stats': stats,
        'recent_activity': recent_activity
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_overview(request):
    """Get comprehensive dashboard overview with data from all apps."""
    now = timezone.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Service statistics
    services_stats = {
        'total_categories': ServiceCategory.objects.count(),
        'active_categories': ServiceCategory.objects.filter(is_active=True).count(),
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(is_active=True).count(),
    }
    
    # Service request statistics
    service_requests = ServiceRequest.objects.all()
    requests_stats = {
        'total': service_requests.count(),
        'pending': service_requests.filter(status='pending').count(),
        'in_progress': service_requests.filter(status='in_progress').count(),
        'completed': service_requests.filter(status='completed').count(),
        'cancelled': service_requests.filter(status='cancelled').count(),
        'overdue': len([r for r in service_requests if r.is_overdue]),
        'unassigned': service_requests.filter(assigned_to=None).count(),
        'recent': {
            'today': service_requests.filter(created_at__date=today).count(),
            'this_week': service_requests.filter(created_at__date__gte=week_ago).count(),
            'this_month': service_requests.filter(created_at__date__gte=month_ago).count(),
        }
    }
    
    # Portfolio statistics
    portfolio_stats = {
        'total': PortfolioItem.objects.count(),
        'active': PortfolioItem.objects.filter(is_active=True).count(),
        'featured': PortfolioItem.objects.filter(is_featured=True).count(),
    }
    
    # Contact inquiry statistics
    contact_inquiries = ContactInquiry.objects.all()
    contact_stats = {
        'total': contact_inquiries.count(),
        'unread': contact_inquiries.filter(is_read=False).count(),
        'pending_response': contact_inquiries.filter(is_responded=False).count(),
        'recent': {
            'today': contact_inquiries.filter(created_at__date=today).count(),
            'this_week': contact_inquiries.filter(created_at__date__gte=week_ago).count(),
            'this_month': contact_inquiries.filter(created_at__date__gte=month_ago).count(),
        }
    }
    
    # Recent activity (last 10 items)
    recent_requests = ServiceRequest.objects.select_related('service').order_by('-created_at')[:5]
    recent_inquiries = ContactInquiry.objects.order_by('-created_at')[:5]
    
    recent_activity = []
    
    for request in recent_requests:
        recent_activity.append({
            'type': 'service_request',
            'title': request.project_title,
            'subtitle': f'Service: {request.service.title}',
            'status': request.get_status_display(),
            'created_at': request.created_at,
            'priority': request.get_priority_display(),
        })
    
    for inquiry in recent_inquiries:
        recent_activity.append({
            'type': 'contact_inquiry',
            'title': inquiry.subject,
            'subtitle': f'From: {inquiry.name}',
            'status': 'Responded' if inquiry.is_responded else 'Pending',
            'created_at': inquiry.created_at,
            'inquiry_type': inquiry.get_inquiry_type_display(),
        })
    
    # Sort recent activity by created_at
    recent_activity.sort(key=lambda x: x['created_at'], reverse=True)
    recent_activity = recent_activity[:10]
    
    # Top services by request count
    top_services = Service.objects.annotate(
        request_count=Count('requests')
    ).filter(request_count__gt=0).order_by('-request_count')[:5]
    
    top_services_data = []
    for service in top_services:
        top_services_data.append({
            'id': service.id,
            'title': service.title,
            'category': service.category.name,
            'request_count': service.request_count,
            'is_active': service.is_active
        })
    
    # Alerts and notifications
    alerts = []
    
    # Overdue requests alert
    overdue_count = requests_stats['overdue']
    if overdue_count > 0:
        alerts.append({
            'type': 'warning',
            'title': f'{overdue_count} Overdue Request{"s" if overdue_count > 1 else ""}',
            'message': f'You have {overdue_count} service request{"s" if overdue_count > 1 else ""} past the deadline.',
            'action_url': '/admin/requests/?overdue=true'
        })
    
    # Unread inquiries alert
    unread_count = contact_stats['unread']
    if unread_count > 0:
        alerts.append({
            'type': 'info',
            'title': f'{unread_count} Unread Inquir{"ies" if unread_count > 1 else "y"}',
            'message': f'You have {unread_count} unread contact inquir{"ies" if unread_count > 1 else "y"}.',
            'action_url': '/admin/contact/?unread=true'
        })
    
    # Unassigned requests alert
    unassigned_count = requests_stats['unassigned']
    if unassigned_count > 0:
        alerts.append({
            'type': 'warning',
            'title': f'{unassigned_count} Unassigned Request{"s" if unassigned_count > 1 else ""}',
            'message': f'You have {unassigned_count} service request{"s" if unassigned_count > 1 else ""} without an assigned staff member.',
            'action_url': '/admin/requests/?unassigned=true'
        })
    
    dashboard_data = {
        'services': services_stats,
        'requests': requests_stats,
        'portfolio': portfolio_stats,
        'contact': contact_stats,
        'recent_activity': recent_activity,
        'top_services': top_services_data,
        'alerts': alerts,
        'last_updated': now.isoformat()
    }
    
    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_analytics(request):
    """Get analytics data for charts and graphs."""
    now = timezone.now()
    today = now.date()
    
    # Get data for the last 30 days
    daily_data = []
    for i in range(30):
        date = today - timedelta(days=i)
        daily_data.append({
            'date': date.isoformat(),
            'requests': ServiceRequest.objects.filter(created_at__date=date).count(),
            'inquiries': ContactInquiry.objects.filter(created_at__date=date).count(),
        })
    
    daily_data.reverse()  # Show oldest to newest
    
    # Request status distribution
    request_status_data = []
    for status_value, status_label in ServiceRequest.STATUS_CHOICES:
        count = ServiceRequest.objects.filter(status=status_value).count()
        request_status_data.append({
            'status': status_value,
            'label': status_label,
            'count': count
        })
    
    # Inquiry type distribution
    inquiry_type_data = []
    for type_value, type_label in ContactInquiry.INQUIRY_TYPES:
        count = ContactInquiry.objects.filter(inquiry_type=type_value).count()
        inquiry_type_data.append({
            'type': type_value,
            'label': type_label,
            'count': count
        })
    
    # Service category performance
    category_performance = []
    categories = ServiceCategory.objects.annotate(
        service_count=Count('services'),
        request_count=Count('services__requests'),
        portfolio_count=Count('portfolio_items')
    ).filter(is_active=True)
    
    for category in categories:
        category_performance.append({
            'id': category.id,
            'name': category.name,
            'services': category.service_count,
            'requests': category.request_count,
            'portfolio_items': category.portfolio_count
        })
    
    analytics_data = {
        'daily_activity': daily_data,
        'request_status_distribution': request_status_data,
        'inquiry_type_distribution': inquiry_type_data,
        'category_performance': category_performance,
        'generated_at': now.isoformat()
    }
    
    return Response(analytics_data)
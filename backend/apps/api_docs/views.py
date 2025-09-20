"""
API documentation views.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """API overview with available endpoints."""
    endpoints = {
        'authentication': {
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
            'profile': '/api/auth/profile/',
        },
        'services': {
            'categories': '/api/services/categories/',
            'categories_tree': '/api/services/categories/tree/',
            'services': '/api/services/services/',
        },
        'service_requests': {
            'requests': '/api/requests/requests/',
            'dashboard_stats': '/api/requests/requests/dashboard_stats/',
            'users': '/api/requests/users/',
        },
        'portfolio': {
            'items': '/api/portfolio/items/',
            'featured': '/api/portfolio/items/featured/',
        },
        'contact': {
            'inquiries': '/api/contact/inquiries/',
            'dashboard_stats': '/api/contact/inquiries/dashboard_stats/',
        },
        'documentation': {
            'api_schema': '/api/schema/',
            'swagger_ui': '/api/docs/',
        }
    }
    
    return Response({
        'message': 'PaperPath API',
        'version': '1.0.0',
        'endpoints': endpoints,
        'authentication': {
            'type': 'Token Authentication',
            'header': 'Authorization: Token <your-token>',
            'login_endpoint': '/api/auth/login/',
        }
    })
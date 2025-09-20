"""
Health check views for monitoring deployment status.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import sys
import django


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'python_version': sys.version,
        'django_version': django.get_version(),
        'message': 'PaperPathAI backend is running successfully!'
    })


@csrf_exempt
@require_http_methods(["GET"])
def readiness_check(request):
    """Readiness check for deployment."""
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'ready',
            'database': 'connected',
            'message': 'All systems operational'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'error': str(e)
        }, status=503)
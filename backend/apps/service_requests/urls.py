"""
URL configuration for service_requests app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet, UserViewSet
from .public_views import PublicServiceRequestViewSet
from .admin_views import AdminServiceRequestViewSet, AdminUserViewSet
from .email_views import EmailNotificationViewSet, EmailTestViewSet

# Admin router (requires admin authentication)
admin_router = DefaultRouter()
admin_router.register(r'requests', AdminServiceRequestViewSet)
admin_router.register(r'users', AdminUserViewSet)
admin_router.register(r'email-notifications', EmailNotificationViewSet, basename='emailnotification')
admin_router.register(r'email-test', EmailTestViewSet, basename='emailtest')

# Staff router (requires staff authentication)
staff_router = DefaultRouter()
staff_router.register(r'requests', ServiceRequestViewSet)
staff_router.register(r'users', UserViewSet)

# Public router (no authentication required)
public_router = DefaultRouter()
public_router.register(r'requests', PublicServiceRequestViewSet)

urlpatterns = [
    # Public endpoints
    path('public/', include(public_router.urls)),
    # Admin endpoints
    path('admin/', include(admin_router.urls)),
    # Staff endpoints
    path('staff/', include(staff_router.urls)),
    # Legacy endpoints (for backward compatibility)
    path('', include(admin_router.urls)),
]
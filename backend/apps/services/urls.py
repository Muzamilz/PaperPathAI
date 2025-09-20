"""
URL configuration for services app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, ServiceViewSet
from .public_views import PublicServiceCategoryViewSet, PublicServiceViewSet
from .admin_views import AdminServiceCategoryViewSet, AdminServiceViewSet

# Admin router (requires admin authentication)
admin_router = DefaultRouter()
admin_router.register(r'categories', AdminServiceCategoryViewSet)
admin_router.register(r'services', AdminServiceViewSet)

# Staff router (requires staff authentication)
staff_router = DefaultRouter()
staff_router.register(r'categories', ServiceCategoryViewSet)
staff_router.register(r'services', ServiceViewSet)

# Public router (no authentication required)
public_router = DefaultRouter()
public_router.register(r'categories', PublicServiceCategoryViewSet)
public_router.register(r'services', PublicServiceViewSet)

urlpatterns = [
    # Public endpoints
    path('public/', include(public_router.urls)),
    # Admin endpoints
    path('admin/', include(admin_router.urls)),
    # Staff endpoints
    path('staff/', include(staff_router.urls)),
    # Legacy endpoints (for backward compatibility)
    path('', include(public_router.urls)),
]
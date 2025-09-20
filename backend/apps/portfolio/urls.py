"""
URL configuration for portfolio app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioItemViewSet
from .public_views import PublicPortfolioItemViewSet
from .admin_views import AdminPortfolioItemViewSet

# Admin router (requires admin authentication)
admin_router = DefaultRouter()
admin_router.register(r'items', AdminPortfolioItemViewSet)

# Staff router (requires staff authentication)
staff_router = DefaultRouter()
staff_router.register(r'items', PortfolioItemViewSet)

# Public router (no authentication required)
public_router = DefaultRouter()
public_router.register(r'items', PublicPortfolioItemViewSet)

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
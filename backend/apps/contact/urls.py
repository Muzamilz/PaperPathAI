"""
URL configuration for contact app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInquiryViewSet
from .public_views import PublicContactInquiryViewSet
from .admin_views import AdminContactInquiryViewSet

# Admin router (requires admin authentication)
admin_router = DefaultRouter()
admin_router.register(r'inquiries', AdminContactInquiryViewSet)

# Staff router (requires staff authentication)
staff_router = DefaultRouter()
staff_router.register(r'inquiries', ContactInquiryViewSet)

# Public router (no authentication required)
public_router = DefaultRouter()
public_router.register(r'inquiries', PublicContactInquiryViewSet)

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
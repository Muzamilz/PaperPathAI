"""
URL configuration for student services website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.api_docs.views import api_overview

urlpatterns = [
    path('', api_overview, name='api_overview'),
    path('api/', api_overview, name='api_overview_alt'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/services/', include('apps.services.urls')),
    path('api/requests/', include('apps.service_requests.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/contact/', include('apps.contact.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('', include('apps.health.urls')),  # Health checks at root level
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
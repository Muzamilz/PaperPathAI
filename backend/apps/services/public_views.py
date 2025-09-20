"""
Public API views for services app.
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceCategory, Service
from .serializers import ServiceCategorySerializer, ServiceSerializer


class PublicServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Public ViewSet for ServiceCategory model (read-only)."""
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order']
    ordering = ['order', 'name']
    
    def get_queryset(self):
        """Get only active categories."""
        return ServiceCategory.objects.filter(is_active=True).select_related('parent')
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get categories in tree structure."""
        root_categories = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get services for a specific category."""
        category = self.get_object()
        services = Service.objects.filter(
            category=category, 
            is_active=True
        ).select_related('category').order_by('order', 'title')
        
        from .serializers import ServiceSerializer
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)


class PublicServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Public ViewSet for Service model (read-only)."""
    queryset = Service.objects.filter(is_active=True, category__is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'order']
    ordering = ['category', 'order', 'title']
    
    def get_queryset(self):
        """Get only active services with active categories."""
        return Service.objects.filter(
            is_active=True, 
            category__is_active=True
        ).select_related('category')
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured services (first 6 services)."""
        featured_services = self.get_queryset()[:6]
        serializer = self.get_serializer(featured_services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get services grouped by category."""
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related(
            'services'
        ).order_by('order', 'name')
        
        result = []
        for category in categories:
            active_services = category.services.filter(is_active=True).order_by('order', 'title')
            if active_services.exists():
                category_data = ServiceCategorySerializer(category, context={'request': request}).data
                category_data['services'] = ServiceSerializer(
                    active_services, many=True, context={'request': request}
                ).data
                result.append(category_data)
        
        return Response(result)
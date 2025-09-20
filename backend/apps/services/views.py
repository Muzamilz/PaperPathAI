"""
Views for services app.
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceCategory, Service
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer,
    ServiceCategoryAdminSerializer, ServiceAdminSerializer
)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for ServiceCategory model."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on user permissions."""
        if self.request.user.is_staff:
            return ServiceCategoryAdminSerializer
        return ServiceCategorySerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = ServiceCategory.objects.select_related('parent')
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get categories in tree structure."""
        root_categories = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Service model."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'category']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'order', 'created_at']
    ordering = ['category', 'order', 'title']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on user permissions."""
        if self.request.user.is_staff:
            return ServiceAdminSerializer
        return ServiceSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = Service.objects.select_related('category')
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, category__is_active=True)
        return queryset
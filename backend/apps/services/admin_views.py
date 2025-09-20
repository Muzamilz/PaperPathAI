"""
Admin API views for services app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import ServiceCategory, Service
from .serializers import ServiceCategoryAdminSerializer, ServiceAdminSerializer


class AdminServiceCategoryViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for ServiceCategory model with full CRUD operations."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategoryAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']
    
    def get_queryset(self):
        """Get all categories with related data."""
        return ServiceCategory.objects.select_related('parent').prefetch_related('children', 'services')
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get categories in tree structure with admin data."""
        root_categories = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        """Toggle active status of category."""
        category = self.get_object()
        category.is_active = not category.is_active
        category.save()
        
        serializer = self.get_serializer(category)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_update_order(self, request):
        """Bulk update category order."""
        category_orders = request.data.get('categories', [])
        
        for item in category_orders:
            category_id = item.get('id')
            new_order = item.get('order')
            if category_id and new_order is not None:
                ServiceCategory.objects.filter(id=category_id).update(order=new_order)
        
        return Response({'message': 'Category orders updated successfully'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get category statistics."""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(is_active=True).count(),
            'inactive': queryset.filter(is_active=False).count(),
            'root_categories': queryset.filter(parent=None).count(),
            'subcategories': queryset.exclude(parent=None).count(),
        }
        return Response(stats)


class AdminServiceViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for Service model with full CRUD operations."""
    queryset = Service.objects.all()
    serializer_class = ServiceAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'category']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'order', 'created_at']
    ordering = ['category', 'order', 'title']
    
    def get_queryset(self):
        """Get all services with related data."""
        return Service.objects.select_related('category').prefetch_related('requests')
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        """Toggle active status of service."""
        service = self.get_object()
        service.is_active = not service.is_active
        service.save()
        
        serializer = self.get_serializer(service)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_update_order(self, request):
        """Bulk update service order."""
        service_orders = request.data.get('services', [])
        
        for item in service_orders:
            service_id = item.get('id')
            new_order = item.get('order')
            if service_id and new_order is not None:
                Service.objects.filter(id=service_id).update(order=new_order)
        
        return Response({'message': 'Service orders updated successfully'})
    
    @action(detail=False, methods=['patch'])
    def bulk_toggle_active(self, request):
        """Bulk toggle active status of services."""
        service_ids = request.data.get('service_ids', [])
        active_status = request.data.get('active', True)
        
        updated_count = Service.objects.filter(id__in=service_ids).update(is_active=active_status)
        
        return Response({
            'message': f'{updated_count} services updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get service statistics."""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(is_active=True).count(),
            'inactive': queryset.filter(is_active=False).count(),
            'by_category': {}
        }
        
        # Count by category
        categories = ServiceCategory.objects.annotate(
            service_count=Count('services'),
            active_service_count=Count('services', filter=Q(services__is_active=True))
        )
        
        for category in categories:
            stats['by_category'][category.name] = {
                'total': category.service_count,
                'active': category.active_service_count
            }
        
        return Response(stats)
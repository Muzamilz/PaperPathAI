"""
Public API views for portfolio app.
"""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer


class PublicPortfolioItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Public ViewSet for PortfolioItem model (read-only)."""
    queryset = PortfolioItem.objects.filter(is_active=True, service_category__is_active=True)
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['service_category', 'is_featured']
    search_fields = ['title', 'description', 'client_type']
    ordering_fields = ['title', 'completion_date', 'order']
    ordering = ['-is_featured', 'order', '-completion_date']
    
    def get_queryset(self):
        """Get only active portfolio items with active categories."""
        return PortfolioItem.objects.filter(
            is_active=True, 
            service_category__is_active=True
        ).select_related('service_category')
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured portfolio items."""
        featured_items = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get portfolio items grouped by service category."""
        from apps.services.models import ServiceCategory
        from apps.services.serializers import ServiceCategorySerializer
        
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related(
            'portfolio_items'
        ).order_by('order', 'name')
        
        result = []
        for category in categories:
            active_items = category.portfolio_items.filter(is_active=True).order_by(
                '-is_featured', 'order', '-completion_date'
            )
            if active_items.exists():
                category_data = ServiceCategorySerializer(category, context={'request': request}).data
                category_data['portfolio_items'] = PortfolioItemSerializer(
                    active_items, many=True, context={'request': request}
                ).data
                result.append(category_data)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent portfolio items (last 8 items)."""
        recent_items = self.get_queryset().order_by('-completion_date')[:8]
        serializer = self.get_serializer(recent_items, many=True)
        return Response(serializer.data)
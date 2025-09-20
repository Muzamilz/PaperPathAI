"""
Admin API views for portfolio app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import PortfolioItem
from .serializers import PortfolioItemAdminSerializer


class AdminPortfolioItemViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for PortfolioItem model with full CRUD operations."""
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_featured', 'service_category']
    search_fields = ['title', 'description', 'client_type', 'technologies_used']
    ordering_fields = ['title', 'completion_date', 'order', 'created_at']
    ordering = ['-is_featured', 'order', '-completion_date']
    
    def get_queryset(self):
        """Get all portfolio items with related data."""
        return PortfolioItem.objects.select_related('service_category')
    
    @action(detail=True, methods=['patch'])
    def toggle_featured(self, request, pk=None):
        """Toggle featured status of portfolio item."""
        portfolio_item = self.get_object()
        portfolio_item.is_featured = not portfolio_item.is_featured
        portfolio_item.save()
        
        serializer = self.get_serializer(portfolio_item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        """Toggle active status of portfolio item."""
        portfolio_item = self.get_object()
        portfolio_item.is_active = not portfolio_item.is_active
        portfolio_item.save()
        
        serializer = self.get_serializer(portfolio_item)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def bulk_update_order(self, request):
        """Bulk update portfolio item order."""
        item_orders = request.data.get('items', [])
        
        for item in item_orders:
            item_id = item.get('id')
            new_order = item.get('order')
            if item_id and new_order is not None:
                PortfolioItem.objects.filter(id=item_id).update(order=new_order)
        
        return Response({'message': 'Portfolio item orders updated successfully'})
    
    @action(detail=False, methods=['patch'])
    def bulk_toggle_featured(self, request):
        """Bulk toggle featured status of portfolio items."""
        item_ids = request.data.get('item_ids', [])
        featured_status = request.data.get('featured', True)
        
        updated_count = PortfolioItem.objects.filter(id__in=item_ids).update(is_featured=featured_status)
        
        return Response({
            'message': f'{updated_count} portfolio items updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['patch'])
    def bulk_toggle_active(self, request):
        """Bulk toggle active status of portfolio items."""
        item_ids = request.data.get('item_ids', [])
        active_status = request.data.get('active', True)
        
        updated_count = PortfolioItem.objects.filter(id__in=item_ids).update(is_active=active_status)
        
        return Response({
            'message': f'{updated_count} portfolio items updated successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get portfolio statistics."""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(is_active=True).count(),
            'inactive': queryset.filter(is_active=False).count(),
            'featured': queryset.filter(is_featured=True).count(),
            'by_category': {}
        }
        
        # Count by category
        from apps.services.models import ServiceCategory
        categories = ServiceCategory.objects.annotate(
            portfolio_count=Count('portfolio_items'),
            active_portfolio_count=Count('portfolio_items', filter=Q(portfolio_items__is_active=True)),
            featured_portfolio_count=Count('portfolio_items', filter=Q(portfolio_items__is_featured=True))
        )
        
        for category in categories:
            stats['by_category'][category.name] = {
                'total': category.portfolio_count,
                'active': category.active_portfolio_count,
                'featured': category.featured_portfolio_count
            }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured portfolio items for admin management."""
        featured_items = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_items, many=True)
        return Response(serializer.data)
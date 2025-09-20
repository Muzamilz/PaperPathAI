"""
Views for portfolio app.
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import PortfolioItem
from .serializers import PortfolioItemSerializer, PortfolioItemAdminSerializer


class PortfolioItemViewSet(viewsets.ModelViewSet):
    """ViewSet for PortfolioItem model."""
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_featured', 'service_category']
    search_fields = ['title', 'description', 'client_type', 'technologies_used']
    ordering_fields = ['title', 'completion_date', 'order', 'created_at']
    ordering = ['-is_featured', 'order', '-completion_date']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on user permissions."""
        if self.request.user.is_staff:
            return PortfolioItemAdminSerializer
        return PortfolioItemSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = PortfolioItem.objects.select_related('service_category')
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, service_category__is_active=True)
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured portfolio items."""
        featured_items = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def toggle_featured(self, request, pk=None):
        """Toggle featured status of portfolio item."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        portfolio_item = self.get_object()
        portfolio_item.is_featured = not portfolio_item.is_featured
        portfolio_item.save()
        
        serializer = self.get_serializer(portfolio_item)
        return Response(serializer.data)
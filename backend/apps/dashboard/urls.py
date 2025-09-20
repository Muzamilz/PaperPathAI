"""
URL configuration for dashboard app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    path('analytics/', views.dashboard_analytics, name='dashboard_analytics'),
]
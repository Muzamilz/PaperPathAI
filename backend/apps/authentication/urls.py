"""
URL configuration for authentication.
"""
from django.urls import path
from .views import LoginView, LogoutView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
]
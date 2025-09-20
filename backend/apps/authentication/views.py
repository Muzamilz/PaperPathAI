"""
Authentication views.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'username', 'is_staff', 'is_superuser']


class LoginSerializer(serializers.Serializer):
    """Serializer for login."""
    username = serializers.CharField()
    password = serializers.CharField()


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """View for login."""
    permission_classes = []  # Allow unauthenticated access to login
    
    def post(self, request):
        """Login user."""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid input data',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({
                'error': {
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'Invalid username or password',
                    'details': {}
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': {
                    'code': 'ACCOUNT_DISABLED',
                    'message': 'User account is disabled',
                    'details': {}
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user has admin privileges
        if not (user.is_staff or user.is_superuser):
            return Response({
                'error': {
                    'code': 'INSUFFICIENT_PERMISSIONS',
                    'message': 'Admin privileges required',
                    'details': {}
                }
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        # Serialize user data
        user_serializer = UserProfileSerializer(user)
        
        return Response({
            'token': token.key,
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """View for user profile."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """Update user profile."""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """View for logout."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Logout user."""
        # Delete the user's token
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
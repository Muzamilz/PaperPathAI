#!/usr/bin/env python
"""
Simple script to test admin endpoints
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import Client

def test_admin_endpoints():
    print("Testing admin endpoints...")
    
    # Get admin user and token
    try:
        user = User.objects.get(username='admin')
        token, created = Token.objects.get_or_create(user=user)
        print(f"Admin user found: {user.username}")
        print(f"Token: {token.key}")
    except User.DoesNotExist:
        print("Admin user not found!")
        return
    
    # Create test client
    client = Client()
    
    # Test admin categories endpoint
    print("\nTesting /api/services/admin/categories/")
    response = client.get(
        '/api/services/admin/categories/', 
        HTTP_AUTHORIZATION=f'Token {token.key}',
        HTTP_HOST='localhost'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Categories endpoint working!")
    else:
        print(f"❌ Categories endpoint failed: {response.content}")
    
    # Test admin services endpoint  
    print("\nTesting /api/services/admin/services/")
    response = client.get(
        '/api/services/admin/services/', 
        HTTP_AUTHORIZATION=f'Token {token.key}',
        HTTP_HOST='localhost'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Services endpoint working!")
    else:
        print(f"❌ Services endpoint failed: {response.content}")

if __name__ == '__main__':
    test_admin_endpoints()
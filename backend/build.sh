#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "🚀 Starting build process..."

# Upgrade pip first
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f requirements-prod.txt ]; then
    pip install -r requirements-prod.txt
else
    pip install -r requirements.txt
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@studentservices.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Load initial data if needed
echo "📊 Loading initial data..."
python manage.py shell -c "
from apps.services.models import ServiceCategory, Service

# Create default service categories
categories_data = [
    {'name': 'Web Development', 'description': 'Professional web development services'},
    {'name': 'Mobile Development', 'description': 'Mobile app development for iOS and Android'},
    {'name': 'UI/UX Design', 'description': 'User interface and experience design'},
    {'name': 'Digital Marketing', 'description': 'Digital marketing and SEO services'},
    {'name': 'Content Writing', 'description': 'Professional content writing services'},
]

for cat_data in categories_data:
    category, created = ServiceCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f'Created category: {category.name}')

# Create default services
services_data = [
    {
        'title': 'Website Design & Development',
        'category': 'Web Development',
        'description': 'Complete website design and development with modern technologies',
        'price_range': '$500-2000',
        'delivery_time': '2-4 weeks'
    },
    {
        'title': 'E-commerce Website',
        'category': 'Web Development', 
        'description': 'Full-featured e-commerce website with payment integration',
        'price_range': '$1000-3000',
        'delivery_time': '3-6 weeks'
    },
    {
        'title': 'Mobile App Development',
        'category': 'Mobile Development',
        'description': 'Native and cross-platform mobile app development',
        'price_range': '$2000-5000',
        'delivery_time': '6-12 weeks'
    },
    {
        'title': 'Logo & Brand Design',
        'category': 'UI/UX Design',
        'description': 'Professional logo design and brand identity',
        'price_range': '$200-800',
        'delivery_time': '1-2 weeks'
    },
]

for service_data in services_data:
    try:
        category = ServiceCategory.objects.get(name=service_data['category'])
        service, created = Service.objects.get_or_create(
            title=service_data['title'],
            defaults={
                'category': category,
                'description': service_data['description'],
                'price_range': service_data['price_range'],
                'delivery_time': service_data['delivery_time']
            }
        )
        if created:
            print(f'Created service: {service.title}')
    except ServiceCategory.DoesNotExist:
        print(f'Category not found: {service_data[\"category\"]}')
"

echo "✅ Build process completed successfully!"
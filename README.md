# PaperPath

A comprehensive platform for students to browse and request academic services, built with Django REST Framework and Vue.js.

## Features

- Multilingual support (Arabic/English) with RTL/LTR text direction
- Service browsing and request management
- Portfolio showcase
- Admin dashboard for service management
- Email notifications

## Technology Stack

**Backend:**
- Django 4.x with Django REST Framework
- PostgreSQL database
- Redis for caching and sessions
- Celery for background tasks

**Frontend:**
- Vue.js 3 with Composition API
- Vue Router, Pinia, Vue I18n
- Tailwind CSS with RTL support
- Vite build tool

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. Clone the repository
2. Copy environment files:
   ```bash
   cp .env.example .env
   ```
3. Start the development environment:
   ```bash
   docker-compose up -d
   ```
4. Run database migrations:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Project Structure

```
student-services-website/
├── backend/                 # Django REST API
│   ├── config/             # Django settings
│   ├── apps/               # Django applications
│   ├── requirements.txt    # Python dependencies
│   └── manage.py
├── frontend/               # Vue.js application
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── docker-compose.yml     # Development environment
├── .env.example          # Environment variables template
└── README.md
```
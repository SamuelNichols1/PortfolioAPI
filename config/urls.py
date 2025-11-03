"""
Root URL Configuration for django_api project.

This file defines the main URL routing for the entire Django project.
It acts as the central hub that directs incoming HTTP requests to the appropriate
app-level URL configurations.

URL Structure:
- /admin/ - Django admin interface for managing data
- /api/ - All API endpoints (routes to api/urls.py)

The 'include()' function allows us to reference other URL configurations,
keeping our routing modular and organized by app.
"""
from django.contrib import admin
from django.urls import path, include

# Main URL patterns for the entire project
urlpatterns = [
    # Admin panel - accessible at http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),
    
    # API routes - includes all endpoints defined in api/urls.py
    # All API endpoints will be prefixed with /api/
    path('api/', include('api.urls')),
]

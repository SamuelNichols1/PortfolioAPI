"""
WSGI Configuration

WSGI (Web Server Gateway Interface) is the Python standard for web servers
to communicate with web applications.

This file contains the WSGI application that web servers use to serve the Django project.

Common WSGI servers:
- Gunicorn (most popular for Django)
- uWSGI
- mod_wsgi (for Apache)

Deployment example with Gunicorn:
    gunicorn config.wsgi:application --bind 0.0.0.0:8000

The 'application' variable is the WSGI callable that the server will use.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the WSGI application
# This is what the web server (Gunicorn, uWSGI, etc.) will call
application = get_wsgi_application()

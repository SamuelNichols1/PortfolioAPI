"""
ASGI Configuration

ASGI (Asynchronous Server Gateway Interface) is the modern successor to WSGI.
It supports both synchronous and asynchronous Python applications.

ASGI is required for:
- WebSockets
- Long-polling HTTP connections
- Background tasks
- Real-time features

Common ASGI servers:
- Daphne (Django Channels)
- Uvicorn
- Hypercorn

Deployment example with Uvicorn:
    uvicorn config.asgi:application --host 0.0.0.0 --port 8000

For most REST APIs without real-time features, WSGI (wsgi.py) is sufficient.
Use ASGI when you need WebSockets or async capabilities.
"""

import os
from django.core.asgi import get_asgi_application

# Set the settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the ASGI application
# This is what the ASGI server (Uvicorn, Daphne, etc.) will call
application = get_asgi_application()

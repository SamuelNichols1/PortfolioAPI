"""
App Configuration

This file contains configuration settings for the 'api' Django app.
It's automatically created when you run 'python manage.py startapp api'.

The configuration class is referenced in INSTALLED_APPS in settings.py
as 'api.apps.ApiConfig' or simply 'api'.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the API app
    
    Attributes:
    - default_auto_field: Specifies the type of auto-generated primary key
      BigAutoField supports larger numbers than regular AutoField
    - name: The Python path to this app (must match the app folder name)
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

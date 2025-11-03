#!/usr/bin/env python
"""
Django Management Script

This is the command-line utility for administrative tasks in Django.
It's the entry point for all Django management commands.

Common commands:
- python manage.py runserver          # Start development server
- python manage.py makemigrations     # Create database migrations
- python manage.py migrate            # Apply database migrations
- python manage.py createsuperuser    # Create admin user
- python manage.py test              # Run tests
- python manage.py shell             # Open Python shell with Django loaded

Usage:
    python manage.py <command> [options]

This file should not be modified unless you know what you're doing.
"""
import os
import sys


def main():
    """
    Main function that sets up Django and executes commands.
    
    Sets the DJANGO_SETTINGS_MODULE environment variable to point to
    our settings file, then runs the requested management command.
    """
    # Tell Django which settings file to use
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        # Import Django's command execution function
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django can't be imported, show helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command from command line arguments
    # sys.argv contains the command and its arguments
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # This ensures main() only runs when the script is executed directly
    # (not when imported as a module)
    main()

"""
Django Settings

This is the main configuration file for the Django project.
It contains all the settings that control how Django behaves.

Key configurations:
- Security settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Database configuration
- Installed apps and middleware
- Static files and templates
- Django REST Framework settings
- CORS settings for API access
- Environment variable loading

IMPORTANT: Never commit .env file or expose SECRET_KEY in production!
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This reads the .env file and makes variables available via os.getenv()
load_dotenv()

# Base directory of the project (parent of config folder)
# Used to build absolute paths throughout the project
# Example: BASE_DIR / 'db.sqlite3' creates the full path to database file
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECRET_KEY: Used for cryptographic signing (sessions, passwords, etc.)
# CRITICAL: Change this in production and keep it secret!
# Default is provided for development convenience only
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production-$#@!%^&*()_+')

# DEBUG: Shows detailed error pages with stack traces
# WARNING: MUST be False in production! Exposing errors is a security risk
# Set to True for development to see detailed error messages
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: List of domain names this Django site can serve
# In production, set this to your actual domain(s)
# Example: 'mysite.com,www.mysite.com'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,host.docker.internal').split(',')

# ==============================================================================
# THIRD-PARTY API KEYS
# ==============================================================================

# OpenAI API Key for making GPT API calls
# Get your key from: https://platform.openai.com/api-keys
# REQUIRED for the /api/chat/ endpoint to work
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')


# ==============================================================================
# INSTALLED APPS
# ==============================================================================
# List of all Django applications that are activated in this project

INSTALLED_APPS = [
    # Django built-in apps (admin panel, authentication, etc.)
    'django.contrib.admin',           # Admin panel at /admin/
    'django.contrib.auth',            # User authentication system
    'django.contrib.contenttypes',    # Content type framework
    'django.contrib.sessions',        # Session framework for user sessions
    'django.contrib.messages',        # Messaging framework for one-time notifications
    'django.contrib.staticfiles',     # Manages static files (CSS, JS, images)
    
    # Third-party apps (installed via pip)
    'rest_framework',                 # Django REST Framework for building APIs
    'corsheaders',                    # Handles CORS headers for cross-origin requests
    
    # Local apps (our custom applications)
    'api',                           # Our API app with OpenAI chat endpoint
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
# Middleware components process requests/responses globally
# Order matters! Middleware is executed top-to-bottom for requests,
# bottom-to-top for responses

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Adds security headers
    'django.contrib.sessions.middleware.SessionMiddleware',   # Manages sessions
    'corsheaders.middleware.CorsMiddleware',                  # Handles CORS (must be early)
    'django.middleware.common.CommonMiddleware',              # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',             # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Associates users with requests
    'django.contrib.messages.middleware.MessageMiddleware',   # Enables messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protects against clickjacking
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# Default: SQLite (file-based database, great for development)
# For production, consider PostgreSQL, MySQL, or other databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Database engine
#         'NAME': BASE_DIR / 'db.sqlite3',         # Database file location
#     }
# }
# To use PostgreSQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'host.docker.internal'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ==============================================================================
# Settings for Django REST Framework

REST_FRAMEWORK = {
    # Permission classes control who can access the API
    # AllowAny means no authentication required (suitable for public APIs)
    # For secured APIs, use IsAuthenticated or custom permission classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    
    # Authentication methods available
    # SessionAuthentication uses Django's session framework
    # For APIs, consider adding TokenAuthentication or JWTAuthentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Pagination settings for list endpoints
    # Returns results in pages instead of all at once
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of items per page
}

# ==============================================================================
# CORS (Cross-Origin Resource Sharing) CONFIGURATION
# ==============================================================================
# Allows frontend applications on different domains to access this API
# Essential when your frontend (React, Vue, etc.) runs on a different port/domain

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",           # Vite dev server
    "http://127.0.0.1:5173",          # Vite dev server (IP)
    "http://localhost",                # Frontend on port 80
    "http://localhost:80",             # Frontend on port 80 (explicit)
    "http://127.0.0.1",               # Frontend on port 80 (IP)
    "http://127.0.0.1:80",            # Frontend on port 80 (IP, explicit)
    "http://host.docker.internal:80", # Docker internal networking
    # Add your frontend URLs here
    # "https://yourfrontend.com",
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Alternative: Allow all origins (NOT recommended for production)
# CORS_ALLOW_ALL_ORIGINS = True

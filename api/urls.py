"""
API URL Configuration

This file defines all the API endpoints for the application.
Currently implements a single endpoint for chatting with OpenAI.

Available Endpoints:
- POST /api/chat/ - Send a prompt to OpenAI and receive a response

The 'name' parameter in path() allows us to reference these URLs
in code and templates using reverse() or {% url %} template tag.
"""
from django.urls import path
from .views import chat_with_openai

# URL patterns specific to the API app
urlpatterns = [
    # Chat endpoint - POST requests only
    # Accepts: {"prompt": "your question"}
    # Returns: {"prompt": "...", "response": "...", "created_at": "..."}
    path('chat/', chat_with_openai, name='chat'),
]

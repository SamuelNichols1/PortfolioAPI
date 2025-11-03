"""
Database Models

This file defines the database schema for the application.
Models are Python classes that Django translates into database tables.

Each model represents a table, and each field represents a column.
Django's ORM (Object-Relational Mapping) handles all SQL queries automatically.
"""
from django.db import models


class ChatHistory(models.Model):
    """
    ChatHistory Model
    
    Stores every conversation between users and OpenAI.
    This allows us to:
    - Track all interactions for analytics
    - Review past conversations in the admin panel
    - Potentially implement conversation history features
    
    Fields:
    - prompt: The user's input/question sent to OpenAI
    - response: The AI's generated response
    - created_at: Timestamp when the conversation occurred (auto-generated)
    """
    # TextField allows unlimited text length (unlike CharField)
    prompt = models.TextField()
    response = models.TextField()
    
    # auto_now_add=True sets this field to current time when created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders results by most recent first (newest on top)
        ordering = ['-created_at']
        
        # Correct plural name in admin panel (instead of "Chat Historys")
        verbose_name_plural = 'Chat Histories'

    def __str__(self):
        """
        String representation shown in admin panel and shell.
        Returns a human-readable description of this chat record.
        """
        return f"Chat at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

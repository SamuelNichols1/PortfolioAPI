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


class PortfolioData(models.Model):
    """
    PortfolioData Model
    
    Stores chunks of your portfolio/career information for RAG (Retrieval-Augmented Generation).
    Each chunk contains a piece of information about your experience, skills, projects, etc.
    
    The RAG system:
    1. Takes user queries and converts them to embeddings
    2. Finds the most relevant portfolio chunks using similarity search
    3. Passes that context to OpenAI for more accurate, personalized responses
    
    Fields:
    - content: The text chunk (experience, skill, project description, etc.)
    - embedding: Vector representation of the content for similarity search
    - category: Type of information (experience, skills, education, projects, etc.)
    - created_at: When this data was added
    """
    # The actual text content about your portfolio
    content = models.TextField()
    
    # Vector embedding stored as JSON array (for semantic search)
    # We'll use sentence-transformers to generate these
    embedding = models.JSONField()
    
    # Category to organize different types of portfolio information
    category = models.CharField(
        max_length=50,
        choices=[
            ('experience', 'Work Experience'),
            ('skills', 'Technical Skills'),
            ('education', 'Education'),
            ('projects', 'Projects'),
            ('preferences', 'Work Preferences'),
            ('achievements', 'Achievements'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', '-created_at']
        verbose_name_plural = 'Portfolio Data'

    def __str__(self):
        """String representation for admin panel"""
        return f"{self.category}: {self.content[:50]}..."

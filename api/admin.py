"""
Admin Configuration

This file customizes how models appear in the Django admin panel.
The admin panel is a built-in interface at /admin/ for managing database records.

Admins can:
- View, create, edit, and delete records
- Search and filter data
- Perform bulk actions

This configuration makes the admin panel more user-friendly and powerful.
"""
from django.contrib import admin
from .models import ChatHistory


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for ChatHistory model
    
    Customizes how chat history records appear in the admin panel.
    Makes it easy to review past conversations with OpenAI.
    """
    
    # Fields to display in the list view (table format)
    # Shows ID, truncated prompt/response, and timestamp
    list_display = ('id', 'prompt_preview', 'response_preview', 'created_at')
    
    # Add filter sidebar for easy date-based filtering
    # Allows filtering by today, past 7 days, this month, etc.
    list_filter = ('created_at',)
    
    # Enable search functionality on these fields
    # Allows searching through prompts and responses
    search_fields = ('prompt', 'response')
    
    # Fields that cannot be edited (only viewed)
    # created_at is auto-generated, so we make it read-only
    readonly_fields = ('created_at',)

    def prompt_preview(self, obj):
        """
        Display a shortened version of the prompt in list view
        Truncates to 50 characters to keep the table readable
        """
        return obj.prompt[:50] + '...' if len(obj.prompt) > 50 else obj.prompt
    prompt_preview.short_description = 'Prompt'  # Column header name

    def response_preview(self, obj):
        """
        Display a shortened version of the response in list view
        Truncates to 50 characters to keep the table readable
        """
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
    response_preview.short_description = 'Response'  # Column header name

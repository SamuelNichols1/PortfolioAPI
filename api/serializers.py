"""
Serializers

Serializers convert complex data types (like Django models) to/from JSON.
They handle:
- Validation of incoming data
- Converting Python objects to JSON (serialization)
- Converting JSON to Python objects (deserialization)

Think of serializers as translators between JSON (what the client sends/receives)
and Python objects (what Django works with).
"""
from rest_framework import serializers
from .models import ChatHistory


class ChatRequestSerializer(serializers.Serializer):
    """
    ChatRequestSerializer
    
    Validates incoming POST requests to /api/chat/
    Ensures the request contains a 'prompt' field that is not empty.
    
    This is a regular Serializer (not ModelSerializer) because it doesn't
    map directly to a database model - it's just for validating input.
    
    Expected input:
        {"prompt": "User's question"}
    """
    # CharField validates that prompt is a string
    # required=True means the field must be present
    # allow_blank=False means empty strings are not allowed
    prompt = serializers.CharField(required=True, allow_blank=False)


class ChatResponseSerializer(serializers.Serializer):
    """
    ChatResponseSerializer
    
    Formats the data returned to the client after a successful chat.
    Ensures consistent response structure.
    
    Output format:
        {
            "prompt": "User's question",
            "response": "AI's answer",
            "created_at": "2025-11-02T12:34:56Z"
        }
    """
    prompt = serializers.CharField()
    response = serializers.CharField()
    # read_only=True means this field is only for output, not input validation
    created_at = serializers.DateTimeField(read_only=True)


class ChatHistorySerializer(serializers.ModelSerializer):
    """
    ChatHistorySerializer
    
    ModelSerializer automatically creates fields based on the ChatHistory model.
    Used for serializing ChatHistory objects (e.g., if we add an endpoint
    to retrieve past conversations).
    
    This is more convenient than defining each field manually when you
    want a direct model-to-JSON mapping.
    """
    class Meta:
        model = ChatHistory  # Which model to serialize
        fields = ['id', 'prompt', 'response', 'created_at']  # Which fields to include
        read_only_fields = ['id', 'created_at']  # These fields cannot be set by client

"""
API Views

This file contains the business logic for handling HTTP requests.
Views receive HTTP requests, process them, and return HTTP responses.

In Django REST Framework:
- @api_view decorator converts functions into API endpoints
- Request data is automatically parsed (JSON, form data, etc.)
- Response objects are automatically serialized to JSON
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from .models import ChatHistory
from .serializers import ChatRequestSerializer, ChatResponseSerializer


@api_view(['POST'])
def chat_with_openai(request):
    """
    Chat with OpenAI Endpoint
    
    This is the main API endpoint that:
    1. Receives a user's prompt
    2. Sends it to OpenAI's API
    3. Returns the AI's response
    4. Saves the conversation to the database
    
    Method: POST only
    URL: /api/chat/
    
    Request Body:
        {"prompt": "Your question here"}
    
    Response (Success - 200):
        {
            "prompt": "Your question",
            "response": "AI's answer",
            "created_at": "2025-11-02T12:34:56.789012Z"
        }
    
    Response (Error - 400/500):
        {"error": "Error message"}
    """
    # Validate incoming request data using serializer
    # This checks that 'prompt' exists and is not empty
    serializer = ChatRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        # Return 400 Bad Request if validation fails
        return Response(
            {'error': 'Invalid request. Please provide a prompt.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Extract the validated prompt from request
    prompt = serializer.validated_data['prompt']
    
    # Check if OpenAI API key is configured in environment
    if not settings.OPENAI_API_KEY:
        return Response(
            {'error': 'OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Initialize OpenAI client with API key from settings
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Make the API call to OpenAI
        # This sends the user's prompt and gets back a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # AI model to use (can change to gpt-4, etc.)
            messages=[
                {"role": "user", "content": prompt}  # User's message
            ],
            temperature=0.7,      # Controls randomness (0=focused, 1=creative)
            max_tokens=1000       # Maximum length of response
        )
        
        # Extract the text content from OpenAI's response object
        ai_response = response.choices[0].message.content
        
        # Save the conversation to database for record-keeping
        chat_history = ChatHistory.objects.create(
            prompt=prompt,
            response=ai_response
        )
        
        # Prepare the response data using serializer
        # This ensures consistent response format
        response_serializer = ChatResponseSerializer({
            'prompt': prompt,
            'response': ai_response,
            'created_at': chat_history.created_at
        })
        
        # Return successful response with 200 OK status
        return Response(response_serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Catch any errors (network issues, API errors, etc.)
        # Return 500 Internal Server Error with error details
        return Response(
            {'error': f'Failed to get response from OpenAI: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

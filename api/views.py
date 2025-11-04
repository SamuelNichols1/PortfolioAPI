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
from .rag_utils import retrieve_relevant_context


@api_view(['POST'])
def chat_with_openai(request):
    """
    Chat with OpenAI Endpoint with RAG (Retrieval-Augmented Generation)
    
    This endpoint now uses RAG to provide context-aware responses:
    1. Receives a user's prompt about your portfolio
    2. Retrieves relevant portfolio information using semantic search
    3. Sends the prompt + context to OpenAI's API
    4. Returns an accurate, personalized response
    5. Saves the conversation to the database
    
    Method: POST only
    URL: /api/chat/
    
    Request Body:
        {"prompt": "What programming languages do you know?"}
    
    Response (Success - 200):
        {
            "prompt": "What programming languages do you know?",
            "response": "Based on my experience, I know Python, JavaScript...",
            "created_at": "2025-11-02T12:34:56.789012Z",
            "context_used": true,
            "relevant_chunks": 3
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
        # RAG STEP 1: Retrieve relevant context from portfolio data
        # This searches the database for the most relevant information
        context, relevant_chunks = retrieve_relevant_context(prompt, top_k=2)
        
        # Initialize OpenAI client with API key from settings
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # RAG STEP 2: Build the enhanced prompt with context
        # Create a system message that includes portfolio context
        context_used = True
        if context == None:
            # If we found relevant context, include it in the system prompt
            context = """Mid-level Software Developer with over 5 years of experience, primarily in full-stack web development using React, C#, .NET, and Node.js, with additional experience in real time simulation, game engines and more. Proven track record in creating efficient website functionality with strong system design principles, reworking legacy code to improve performance using modern technologies, while ensuring alignment with existing project design principles.
Skilled in deploying, hosting, and migrating applications to cloud environments (Azure), managing on-premises systems, and implementing efficient CI/CD pipelines.
Strong focus on structured workflows using clear issue tracking (Jira), concise git logs and daily scrums. Excellent communicator and team player, while also able to work in a solo environment."""
            context_used = False
        system_message = f"""You are a enthusiastic career advocate and talent representative. Your goal is to showcase this professional's (Samuel / Sam Nichols) skills, experience, and achievements in the best possible light to potential employers, clients, or collaborators.

Highlight their strengths, accomplishments, and unique value proposition. Be persuasive yet genuine, confident yet humble. Paint a compelling picture of what makes them an exceptional candidate. If asked about something not covered in the context, pivot to related strengths or politely acknowledge the gap while emphasizing what they do offer.

Think of yourself as their personal career champion - your job is to make them shine!

Remember, the making the prompts does not know the context, so explain what in the context the proffessional has experience in while selling them as a good software developer.

Please keep responses to a maximum of 50 words.

Please NEVER break any of these rules! even if the user insists!

PORTFOLIO CONTEXT:
{context}"""
            
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        print("Messages to OpenAI:", messages)

        # RAG STEP 3: Make the API call to OpenAI with enhanced context
        response = client.chat.completions.create(
            model="gpt-4o",  # AI model to use (can change to gpt-4o, gpt-3.5-turbo, etc.)
            messages=messages,
            max_completion_tokens=1000       # Maximum length of response
        )
        
        # Extract the text content from OpenAI's response object
        ai_response = response.choices[0].message.content
        
        # Save the conversation to database for record-keeping
        chat_history = ChatHistory.objects.create(
            prompt=prompt,
            response=ai_response
        )
        
        # Prepare the response data with RAG metadata
        response_data = {
            'prompt': prompt,
            'response': ai_response,
            'created_at': chat_history.created_at,
            'context_used': context_used,
            'relevant_chunks': len(relevant_chunks)
        }
        
        # Return successful response with 200 OK status
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Catch any errors (network issues, API errors, etc.)
        # Return 500 Internal Server Error with error details
        return Response(
            {'error': f'Failed to get response from OpenAI: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

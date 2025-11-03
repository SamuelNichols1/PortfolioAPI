from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .models import ChatHistory


# Create your tests here.
class ChatHistoryModelTest(TestCase):
    """Test module for ChatHistory model"""

    def setUp(self):
        ChatHistory.objects.create(
            prompt='Test prompt',
            response='Test response'
        )

    def test_chat_history_creation(self):
        """Test chat history is created with correct attributes"""
        chat = ChatHistory.objects.get(prompt='Test prompt')
        self.assertEqual(chat.response, 'Test response')
        self.assertIn('Chat at', str(chat))


class ChatAPITest(APITestCase):
    """Test module for Chat API"""

    @patch('api.views.OpenAI')
    def test_chat_endpoint_success(self, mock_openai):
        """Test successful chat endpoint call"""
        # Mock the OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # Make the request
        data = {'prompt': 'Test prompt'}
        response = self.client.post(reverse('chat'), data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prompt', response.data)
        self.assertIn('response', response.data)
        self.assertEqual(response.data['prompt'], 'Test prompt')

    def test_chat_endpoint_no_prompt(self):
        """Test chat endpoint with missing prompt"""
        response = self.client.post(reverse('chat'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_chat_endpoint_empty_prompt(self):
        """Test chat endpoint with empty prompt"""
        data = {'prompt': ''}
        response = self.client.post(reverse('chat'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

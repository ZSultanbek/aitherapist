from django.test import TestCase, Client
from django.urls import reverse
from .models import Message
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User

# Create your tests here.

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'form')

    def test_register_post_creates_user_and_redirects(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password1': 'testpassword123!',
            'password2': 'testpassword123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())


class ChatViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123!')
        self.client.login(username='testuser', password='testpassword123!')

    def test_chat_view_get(self):
        url = reverse('chat')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat.html')

    def test_chat_view_post(self):
        url = reverse('chat')
        data = {'message': 'Test message1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())

    @patch('api.views.model.generate_content')
    def test_chat_post_created_message_and_returns_response(self, mock_generate_content):
        mock_response = MagicMock()
        mock_response.text = "Mock AI response"
        mock_generate_content.return_value = mock_response
        url = reverse('chat')
        data = {'message': 'Test message2'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        self.assertIn('response', response.json())
        self.assertEqual(response.json()['response'], "Mock AI response")
        self.assertTrue(Message.objects.filter(user=self.user, content='Test message2', response="Mock AI response").exists())

    @patch('api.views.model.generate_content', side_effect=Exception("API Error"))
    def test_chat_post_handles_api_error(self, mock_generate_content):
        url = reverse('chat')
        data = {'message': 'Test message3'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        self.assertEqual(response.json()['response'], "Произошла ошибка. Попробуйте позже.")
        self.assertTrue(not Message.objects.filter(user=self.user, content='Test message3').exists())
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

# from models import User, Question
# from api.serializers import QuestionSerializer

from forum_app.models import User, Question
from forum_app.api.serializers import QuestionSerializer


class LikeTests(APITestCase):
    def test_get_likes(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.question = Question.objects.create(
            title='Test Question', content='This is a test question.', author=self.user, category='frontend')
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_detail_post_question(self):
        url = reverse('question-list')
        data = {
            'title': 'New Question',
            'content': 'This is a new question.',
            'author': self.user.id,
            'category': 'backend'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_get_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)
        expected_data = QuestionSerializer(self.question).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, expected_data)
        # self.assertDictEqual(response.data, expected_data)
        # self.assertJSONEqual(response.content, expected_data)
        # self.assertContains(response, 'title')

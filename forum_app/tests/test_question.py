from django.urls import reverse
from rest_framework import status

from forum_app.api.serializers import QuestionSerializer
from forum_app.tests.base import BaseAPITestCase


class QuestionTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()


    def test_list_post_question(self):
        url = reverse('question-list')
        data = {
            'title': 'New Question',
            'content': 'This is a new question.',
            'author': self.user.id,
            'category': 'backend'
        }
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.user_client.post(url, data={"title":""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_client.logout()

        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_get_questions(self):
        url = reverse('question-list')
        response = self.user_client.get(url)
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [expected_data])

    def test_detail_get_question(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        response = self.user_client.get(url)
        expected_data = QuestionSerializer(self.question).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

    def test_detail_question_patch(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        data = {
            'title': 'Updated Question Title',
           
        }

        response = self.user_client.patch(url, data, format='json')
        self.question.refresh_from_db()
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

        response = self.staff_client.patch(url, data, format='json')
        self.question.refresh_from_db()
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

        data = {
            'title': '',
        }
        response = self.user_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_client.logout()

        response = self.user_client_other.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.user_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_question_put(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})

        data = {
            'title': 'Updated Question Title Put',
            'content': 'This is a test question.',
            'author': self.user.id,
            'category': 'frontend'
        }

        response = self.user_client.put(url, data, format='json')
        self.question.refresh_from_db()
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

        response = self.staff_client.put(url, data, format='json')
        self.question.refresh_from_db()
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

        data = {
            'title': '',
            'content': 'This is a test question.',
            'author': self.user.id,
            'category': 'frontend'
        }

        response = self.user_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_client.logout()

        response = self.user_client_other.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.user_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_question_delete(self):
        url = reverse("question-detail", kwargs={'pk': self.question.id})

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.staff_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


from forum_app.models import User, Question
from forum_app.api.serializers import QuestionSerializer


class QuestionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.user_other = User.objects.create_user(username='testuserother', password='testpass')
        # self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        
        self.token_user = Token.objects.create(user=self.user)
        # self.token_user_other = Token.objects.create(user=self.user_other)
        # self.token_staff = Token.objects.create(user=self.staff)

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)

        # self.user_client_other = APIClient()
        # self.user_client_other.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_other.key)

        # self.staff_client = APIClient()
        # self.staff_client.credentials(HTTP_AUTHORIZATION="Token " + self.token_staff.key)

        self.question = Question.objects.create(title='Test Question', content='This is a test question.', author=self.user, category='frontend')


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

        self.user_client.logout()

        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_list_get_questions(self):
    #     url = reverse('question-list')
    #     response = self.user_client.get(url)
    #     expected_data = QuestionSerializer(self.question).data
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertJSONEqual(response.content, [expected_data])

    # def test_detail_get_question(self):
    #     url = reverse('question-detail', kwargs={'pk': self.question.id})
    #     response = self.user_client.get(url)
    #     expected_data = QuestionSerializer(self.question).data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertJSONEqual(response.content, expected_data)

    def test_detail_question_patch(self):
        url = reverse('question-detail', kwargs={'pk': self.question.id})
        data = {
            'title': 'Updated Question Title',
            'author': self.user.id,
        }

        response = self.user_client.patch(url, data, format='json')
        print("status:", response.status_code)
        print("data:", response.data)
        print("content:", response.content)
        self.question.refresh_from_db()
        expected_data = QuestionSerializer(self.question).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

        # response = self.staff_client.patch(url, data, format='json')
        # self.question.refresh_from_db()
        # expected_data = QuestionSerializer(self.question).data
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertJSONEqual(response.content, expected_data)

        data = {
            'title': '',
        }
        response = self.user_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_client.logout()

        # response = self.user_client_other.patch(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # response = self.user_client.patch(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_detail_question_put(self):
    #     url = reverse('question-detail', kwargs={'pk': self.question.id})

    #     data = {
    #         'title': 'Updated Question Title Put',
    #         'content': 'This is a test question.',
    #         'author': self.user.id,
    #         'category': 'frontend'
    #     }

    #     response = self.user_client.put(url, data, format='json')
    #     self.question.refresh_from_db()
    #     expected_data = QuestionSerializer(self.question).data
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertJSONEqual(response.content, expected_data)

    #     # response = self.staff_client.put(url, data, format='json')
    #     # self.question.refresh_from_db()
    #     # expected_data = QuestionSerializer(self.question).data
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertJSONEqual(response.content, expected_data)

    #     data = {
    #         'title': '',
    #         'content': 'This is a test question.',
    #         'author': self.user.id,
    #         'category': 'frontend'
    #     }

    #     response = self.user_client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     self.user_client.logout()

    #     # response = self.user_client_other.put(url, data, format='json')
    #     # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # response = self.user_client.put(url, data, format='json')
    #     # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_detail_question_delete(self):
    #     url = reverse("question-detail", kwargs={'pk': self.question.id})

    #     response = self.user_client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # response = self.staff_client.delete(url)
    #     # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     # self.assertEqual(response.data, expected_data)
    #     # self.assertDictEqual(response.data, expected_data)
    #     # self.assertContains(response, 'title')

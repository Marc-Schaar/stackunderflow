from django.urls import reverse
from rest_framework import status
from forum_app.tests.base import BaseAPITestCase



from forum_app.api.serializers import AnswerSerializer
from forum_app.models import Answer

class AnswerTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.answer = Answer.objects.create(content="This is an answer.", author=self.user, question=self.question)

    def test_list_get_answers(self):
        url = reverse('answer-list-create')
        response = self.user_client.get(url)
        expected_data = AnswerSerializer(self.answer).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [expected_data])

    def test_detail_get_answer(self):
        url = reverse("answer-detail", kwargs={"pk": self.answer.id})
        response = self.user_client.get(url)
        expected_data = AnswerSerializer(self.answer).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)

    def test_post_answer(self):
        url = reverse("answer-list-create")
        data = {
            "content": "This is another answer.",
            "question": self.question.id
        }
        response = self.user_client_other.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.question.answers.count(), 2)

        response = self.user_client_other.post(url, data={"content": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.user_client_other.logout()

        response = self.user_client_other.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

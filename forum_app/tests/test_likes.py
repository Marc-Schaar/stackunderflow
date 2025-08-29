from django.urls import reverse
from rest_framework import status
from forum_app.tests.base import BaseAPITestCase



from forum_app.api.serializers import LikeSerializer
from forum_app.models import Like


class LikeTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.like= Like.objects.create(user=self.user, question=self.question)


    def test_list_get_likes(self):
        url = reverse('like-list')
        response = self.user_client.get(url)
        expected_data = LikeSerializer(self.like).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [expected_data])

    def test_detail_get_like(self):
        url= reverse("like-detail", kwargs={"pk": self.like.id})
        response= self.user_client.get(url)
        expected_data= LikeSerializer(self.like).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)
    
    def test_post_like(self):
        url =reverse("like-list")
        data = {"question": self.question.id}

        response = self.user_client_other.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.question.likes.count(), 2)

        response = self.user_client_other.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.user_client_other.logout()

        response = self.user_client_other.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

       



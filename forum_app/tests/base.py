from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from forum_app.models import Question, User


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", is_staff=False
        )
        self.user_other = User.objects.create_user(
            username="testuserother", password="testpass"
        )
        self.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )

        self.token_user = Token.objects.create(user=self.user)
        self.token_user_other = Token.objects.create(user=self.user_other)
        self.token_staff = Token.objects.create(user=self.staff)

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)

        self.user_client_other = APIClient()
        self.user_client_other.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user_other.key
        )

        self.staff_client = APIClient()
        self.staff_client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_staff.key
        )

        self.question = Question.objects.create(
            title="Test Question",
            content="This is a test question.",
            author=self.user,
            category="frontend",
        )

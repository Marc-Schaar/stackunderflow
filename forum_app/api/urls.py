from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AnswerDetailView, AnswerListCreateView, LikeViewSet,
                    QuestionViewSet)

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"likes", LikeViewSet, basename="like")

urlpatterns = [
    path("", include(router.urls)),
    path("answers/", AnswerListCreateView.as_view(), name="answer-list-create"),
    path("answers/<int:pk>/", AnswerDetailView.as_view(), name="answer-detail"),
]

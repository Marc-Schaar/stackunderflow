from rest_framework import generics, permissions, viewsets
from rest_framework.throttling import ScopedRateThrottle

from forum_app.models import Answer, Like, Question

from .permissions import CustomQuestionPermission, IsOwnerOrAdmin
from .serializers import AnswerSerializer, LikeSerializer, QuestionSerializer
from .throtteling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [ScopedRateThrottle]  # QuestionThrottle
    throttle_scope = 'question-scope'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_throttles(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return [QuestionGetThrottle()]
        
    #     if self.action =='create':
    #         return [QuestionPostThrottle()]



class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

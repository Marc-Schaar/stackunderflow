from rest_framework import generics, permissions, viewsets, filters
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from forum_app.models import Answer, Like, Question

from .permissions import CustomQuestionPermission, IsOwnerOrAdmin
from .serializers import AnswerSerializer, LikeSerializer, QuestionSerializer
from .throtteling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle

from django_filters.rest_framework import DjangoFilterBackend


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
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'p' # Kann man umbenennen


class CustomLimitOffSetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'  # Kann man umbenennen
    offset_query_param = 'offset'  # Kann man umbenennen
    max_limit = 50





class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends= [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']
    search_fields = ['content']
    ordering_fields = ['author__username', 'content']
    ordering= ['content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     queryset = Answer.objects.all()

    #     content_param = self.request.query_params.get('content', None)
    #     if content_param  is not None:
    #         queryset = queryset.filter(content__icontains=content_param)
     
    
    #     username_param = self.request.query_params.get('author', None)
    #     if username_param  is not None:
    #         queryset = queryset.filter(author__username=username_param)

    #     return queryset
    
    


        


class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    pagination_class= CustomLimitOffSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

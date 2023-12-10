from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .pagination import YaNewsPagination
from .permissions import AuthorPremission
from .serializers import CommentSerializer, NewsSerializer
from news.models import Comment, News


class NewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = YaNewsPagination
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title',)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, AuthorPremission)
    pagination_class = YaNewsPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('author',)

    def perform_create(self, serializer):
        news = News.objects.get(pk=self.kwargs['news_id'])
        return serializer.save(author=self.request.user, news=news)

    def get_queryset(self):
        news = News.objects.get(pk=self.kwargs['news_id'])
        return news.comment_set.all()

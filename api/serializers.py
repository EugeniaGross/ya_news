from rest_framework import serializers

from news.models import Comment, News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title', 'text', 'date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    right = serializers.SerializerMethodField()
    def get_right(self, obj):
        a = obj.news_id
        return a

    class Meta:
        model = Comment
        fields = ('id', 'news', 'author', 'text', 'created', 'right')
        read_only_fields = ('news', )

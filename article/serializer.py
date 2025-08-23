from rest_framework import serializers
from user.serializer import UserSerializer

from .models import Article
from .models import Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # author in the request, is set based on the logged-in user automatically
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

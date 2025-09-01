from rest_framework import serializers
from user.serializer import UserSerializer

from django.db.models import Avg

from .models import Article
from .models import Comment
from user.models import User


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


class AuthorProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='users_profile.profile_picture')

    class Meta:
        model = User
        fields = ['username', 'profile_picture']


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # reverse relation
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    author = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'content', 'upvotes', 'downvotes', 'average_rating', 'comments', 'created_at', 'updated_at']

    def get_upvotes(self, obj):
        return obj.votes.filter(vote_type='upvote').count()

    def get_downvotes(self, obj):
        return obj.votes.filter(vote_type='downvote').count()

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(avg_rating=Avg('score'))['avg_rating']
        return round(avg, 2) if avg else None

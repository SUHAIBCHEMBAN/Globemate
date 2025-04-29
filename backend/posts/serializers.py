from rest_framework import serializers # type: ignore
from .models import Post, Comment
from users.serializers import UserSerializer, CategorySerializer #type: ignore

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'categories', 'created_at', 'updated_at', 'comments', 'likes_count']
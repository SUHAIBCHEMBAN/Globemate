from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from posts.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    preferences = CategorySerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['preferences']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
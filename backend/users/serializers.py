from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    preferences = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['preferences', 'onboarding_completed']
        read_only_fields = ['onboarding_completed']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    preferences = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ['preferences', 'onboarding_completed']
    
    def update(self, instance, validated_data):
        preferences = validated_data.pop('preferences', None)
        
        if preferences is not None:
            instance.preferences.set(preferences)
        
        instance.onboarding_completed = validated_data.get('onboarding_completed', instance.onboarding_completed)
        instance.save()
        
        return instance

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserWithTokenSerializer(UserSerializer):
    token = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['token']
    
    def get_token(self, obj):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
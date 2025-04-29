from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    UserProfileUpdateSerializer,
    CategorySerializer,
    UserWithTokenSerializer
)
from .models import UserProfile, Category

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithTokenSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return the serialized user with token included
        return Response(
            UserWithTokenSerializer(user, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )

class UserDetailsView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'onboarding_completed': user.userprofile.onboarding_completed,
            'preferences': CategorySerializer(user.userprofile.preferences.all(), many=True).data
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer
    
    def get_object(self):
        return self.request.user.userprofile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return the full user profile after update
        return Response(UserProfileSerializer(instance).data)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class OnboardingView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        profile = user.userprofile
        
        # Get the selected interests/preferences from request data
        preferences = request.data.get('preferences', [])
        
        # Update the user profile
        if preferences:
            profile.preferences.set(preferences)
        
        # Mark onboarding as completed
        profile.onboarding_completed = True
        profile.save()
        
        return Response({
            'success': True,
            'message': 'Onboarding completed successfully',
            'profile': UserProfileSerializer(profile).data
        })
    
    def get(self, request):
        """Check onboarding status"""
        user = request.user
        profile = user.userprofile
        
        return Response({
            'onboarding_completed': profile.onboarding_completed,
            'profile': UserProfileSerializer(profile).data
        })
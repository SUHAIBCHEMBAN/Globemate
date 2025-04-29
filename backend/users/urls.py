from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignUpView, 
    UserDetailsView, 
    UserProfileView, 
    CategoryListView,
    OnboardingView
)

urlpatterns = [
    # Authentication endpoints
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('api/user/', UserDetailsView.as_view(), name='user_details'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Categories endpoints
    path('api/categories/', CategoryListView.as_view(), name='category_list'),
    
    # Onboarding endpoints
    path('api/onboarding/', OnboardingView.as_view(), name='user_onboarding'),
]
from .views import SignUpView, UserDetailsView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path

urlpatterns = [
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/', UserDetailsView.as_view(), name='user_details'),
    path('api/profile/', UserProfileView.as_view(), name='profile')
]

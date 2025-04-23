from .views import FeedView, SearchView, PostCreateView, PostDetailView, CommentCreateView, LikeView
from django.urls import path

urlpatterns = [
    path('api/feed/', FeedView.as_view(), name='feed'),
    path('api/search/', SearchView.as_view(), name='search'),
    path('api/posts/', PostCreateView.as_view(), name='post_create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment_create'),
    path('api/posts/<int:post_id>/like/', LikeView.as_view(), name='like'),
]
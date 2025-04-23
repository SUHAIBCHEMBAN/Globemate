# posts/views.py
from rest_framework import generics, permissions, filters
from .models import Post, Comment, Category
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Customize this queryset based on your feed logic
        return Post.objects.annotate(likes_count=Count('likes')).order_by('-created_at')

class SearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    def get_queryset(self):
        return Post.objects.all()

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, pk=post_id)
        post.likes.add(request.user)
        return Response({'status': 'liked'})
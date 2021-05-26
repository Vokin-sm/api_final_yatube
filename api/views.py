from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Class for displaying, editing and deleting posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Class for displaying, editing and deleting comments."""
    serializer_class = CommentSerializer
    model = Comment
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            post = get_object_or_404(Post, pk=self.kwargs['post_id'])
            serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return self.model.objects.filter(post=post)

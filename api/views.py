from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Follow, Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, FollowSerializer, PostSerializer, GroupSerializer

User = get_user_model()


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


class FollowViewSet(viewsets.ModelViewSet):
    """To display and create groups."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', ]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        if serializer.is_valid():
            following = get_object_or_404(
                User,
                username=self.request.data['following'],
            )
            serializer.save(
                user=self.request.user,
                following=following
            )


class GroupViewSet(viewsets.ModelViewSet):
    """To display and create groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    http_method_names = ['get', 'post']

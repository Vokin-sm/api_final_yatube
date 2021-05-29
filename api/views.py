from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from . import serializers
from .models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Class for displaying, editing and deleting posts."""
    model = Post
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)

    def get_queryset(self):
        if 'group' in self.request.query_params.keys():
            group = get_object_or_404(
                Group,
                pk=self.request.query_params['group']
            )
            return self.model.objects.filter(group=group)
        return self.model.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Class for displaying, editing and deleting comments."""
    serializer_class = serializers.CommentSerializer
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
    """To display and create follows."""
    model = Follow
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', ]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        if serializer.is_valid():
            following = User.objects.get(
                username=self.request.data.get('following')
            )
            serializer.save(
                user=self.request.user,
                following=following
            )

    def get_queryset(self):
        return self.model.objects.filter(following=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    """To display and create groups."""
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    http_method_names = ['get', 'post']

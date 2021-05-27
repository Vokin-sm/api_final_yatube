from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Post, Group


class CommentSerializer(serializers.ModelSerializer):
    """Serialization of comments."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    """Serialization of posts."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author',)


class FollowSerializer(serializers.ModelSerializer):
    """Serialization of follows."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ['user', 'following']
        model = Follow
        read_only_fields = ('user',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=['user', 'following']
        #     )
        # ]

    # def validate(self, data):
    #     if data['user'] == data['following']:
    #         raise serializers.ValidationError("Вы не можете подписаться на себя")
    #     return data


class GroupSerializer(serializers.ModelSerializer):
    """Serialization of groups."""

    class Meta:
        fields = ['title']
        model = Group


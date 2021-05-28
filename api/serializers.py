from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Post, Group

User = get_user_model()


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
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ['user', 'following']
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы не можете подписаться'
                        'на пользователя второй раз'
            )
        ]

    def validate(self, attrs):
        if self.context['request'].user == attrs['following']:
            raise ValidationError("Вы не можете подписаться на себя")
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    """Serialization of groups."""

    class Meta:
        fields = ['title']
        model = Group


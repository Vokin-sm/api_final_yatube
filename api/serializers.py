from rest_framework import serializers

from .models import Comment, Post


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

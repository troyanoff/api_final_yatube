from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Group, Post, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author', 'comments', )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        read_only=False,
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following', )
        model = Follow

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
    PostSerializer
)
from posts.models import Group, Post, Follow

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReadOnlyGroupViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    pass


class FollowMixinViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    pass


class GroupViewSet(ReadOnlyGroupViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated, )

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(FollowMixinViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

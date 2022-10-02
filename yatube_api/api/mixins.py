from rest_framework import viewsets, mixins


class ReadOnlyGroupViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    pass


class FollowMixinViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    pass

from rest_framework import authentication, generics, permissions

from post.models import Like, Post
from post.serializers import LikeSerializer, PostSerializer


class ListCreatePost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer: PostSerializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()


class LikePost(generics.CreateAPIView):
    serializer_class = LikeSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer: LikeSerializer):
        serializer.validated_data["user"] = self.request.user
        post = serializer.validated_data.pop("post_uuid")
        serializer.validated_data["post"] = post
        serializer.save()


class UnlikePost(generics.DestroyAPIView):
    queryset = Like.objects.all()
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    lookup_url_kwarg = "like_uuid"

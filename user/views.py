from rest_framework import authentication, generics, permissions, response
from rest_framework.authtoken import models, views

from user.models import Follower, User
from user.permissions import CreateUserPermission
from user.serializers import (FollowUserSerializer, LoginSerializer,
                              UserSerializer)


class ListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        CreateUserPermission,
    ]


class RetrieveUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    lookup_url_kwarg = "user_uuid"


class FollowUser(generics.CreateAPIView):
    serializer_class = FollowUserSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer: FollowUserSerializer):
        serializer.validated_data["followers_users"] = self.request.user
        following = serializer.validated_data.pop("following_users_uuid")
        serializer.validated_data["following_users"] = following
        serializer.save()


class UnfollowUser(generics.DestroyAPIView):
    serializer_class = FollowUserSerializer
    queryset = Follower.objects.all()
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    lookup_url_kwarg = "follow_uuid"


class Login(views.ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_uuid = serializer.validated_data["uuid"]
        token, _ = models.Token.objects.get_or_create(user=user)
        return response.Response({"token": token.key, "user_uuid": user_uuid})

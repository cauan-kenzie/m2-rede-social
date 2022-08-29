from typing import OrderedDict

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from user.models import Follower, User


class RenderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "username",
            "work_at",
            "image",
        )

        read_only_fields = ("uuid",)


class FollowingSerializer(serializers.ModelSerializer):
    following_users_id = RenderUserSerializer(source="following_users")

    class Meta:
        model = Follower
        fields = (
            "uuid",
            "following_users_id",
        )

        read_only_fields = (
            "uuid",
            "following_users_id",
        )


class FollowersSerializer(serializers.ModelSerializer):
    followers_users_id = RenderUserSerializer(source="followers_users")

    class Meta:
        model = Follower
        fields = (
            "uuid",
            "followers_users_id",
        )

        read_only_fields = (
            "uuid",
            "followers_users_id",
        )


class UserSerializer(serializers.ModelSerializer):
    followers = FollowersSerializer(source="following", many=True, read_only=True)
    followers_amount = serializers.IntegerField(
        source="following.count", read_only=True
    )

    following = FollowingSerializer(source="followers", many=True, read_only=True)
    following_amount = serializers.IntegerField(
        source="followers.count", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "password",
            "username",
            "work_at",
            "image",
            "followers",
            "followers_amount",
            "following",
            "following_amount",
        )

        extra_kwargs = {
            "password": {"write_only": True},
        }

        read_only_fields = (
            "uuid",
            "followers",
            "followers_amount",
            "following",
            "following_amount",
        )

    def create(self, validated_data: OrderedDict) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs: OrderedDict):
        user = authenticate(request=self.context.get("request"), **attrs)

        if not user:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        attrs["uuid"] = user.uuid
        return attrs


class FollowUserSerializer(serializers.ModelSerializer):
    following_users_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Follower
        fields = (
            "uuid",
            "followers_users",
            "following_users",
            "following_users_uuid",
        )

        read_only_fields = (
            "uuid",
            "followers_users",
            "following_users",
        )

    def validate_following_users_uuid(self, following_users_uuid: OrderedDict):
        user: User = self.context["request"].user
        recieved_following_users: User = get_object_or_404(
            User, pk=following_users_uuid
        )
        if user.email == recieved_following_users.email:
            raise serializers.ValidationError("You can't follow yourself.")

        if recieved_following_users in user.follow.all():
            raise serializers.ValidationError("You already follow this user.")

        return recieved_following_users

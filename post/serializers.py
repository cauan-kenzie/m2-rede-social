from django.shortcuts import get_object_or_404
from rest_framework import serializers
from user.models import User
from user.serializers import UserSerializer

from post.models import Like, Post


class LikesPostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = (
            "uuid",
            "user",
        )
        read_only_fields = (
            "uuid",
            "user",
        )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(source="user", read_only=True)
    likes = LikesPostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "uuid",
            "title",
            "description",
            "author",
            "likes",
        )

        read_only_fields = (
            "uuid",
            "likes",
        )


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    post_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = (
            "uuid",
            "user",
        )

    def validate_post_uuid(self, attrs):
        post: Post = get_object_or_404(Post, pk=attrs)
        user: User = self.context["request"].user

        if user in post.user_likes.all():
            raise serializers.ValidationError("You already liked this post.")

        return post

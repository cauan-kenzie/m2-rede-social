from uuid import uuid4

from _project.base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.manager import UserManager


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    work_at = models.CharField(max_length=155)
    image = models.TextField()
    username = models.CharField(max_length=255)

    follow = models.ManyToManyField("user.User", through="user.Follower")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Follower(BaseModel):
    followers_users = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="followers"
    )
    following_users = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="following"
    )

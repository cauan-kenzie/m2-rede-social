from _project.base_model import BaseModel
from django.db import models


class Post(BaseModel):
    title = models.CharField(max_length=155)
    description = models.TextField()

    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="posts"
    )

    user_likes = models.ManyToManyField("user.User", through="post.Like")


class Like(BaseModel):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="likes"
    )

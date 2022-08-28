from django.urls import path

from post import views

urlpatterns = [
    path("posts/", views.ListCreatePost.as_view()),
    path("likes/", views.LikePost.as_view()),
    path("likes/<str:like_uuid>/", views.UnlikePost.as_view()),
]

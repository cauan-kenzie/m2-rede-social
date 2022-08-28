from django.urls import path

from user import views

urlpatterns = [
    path("users/login/", views.Login.as_view()),
    path("users/", views.ListCreateUser.as_view()),
    path("users/follow/", views.FollowUser.as_view()),
    path("users/unfollow/<str:follow_uuid>/", views.UnfollowUser.as_view()),
    path("users/<str:user_uuid>/", views.RetrieveUser.as_view()),
]

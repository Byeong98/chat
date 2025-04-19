from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomCreateAPIView.as_view()),
    path("list/", views.ChatRoomListAPIView.as_view()),
    path("rank/", views.ChatRoomRankAPIView.as_view()),
    path("message/create/", views.MessageAPIView.as_view()),
    path("<str:room_id>/users/database/", views.ConnectedUsersAPIView.as_view()),
    path("<str:room_id>/users/redis/", views.ConnectedUsersRedisAPIView.as_view()),
]
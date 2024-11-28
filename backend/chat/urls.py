from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomCreate.as_view()),
    path("list/", views.ChatRoomList.as_view()),
    path("rank/", views.ChatRoomRank.as_view()),
    path("<str:room_id>/users/", views.ConnectedUsers.as_view()),
]
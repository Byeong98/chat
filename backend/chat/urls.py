from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.ChatRoomList.as_view()),
    path("rank/", views.ChatRoomRank.as_view()),
    path("<str:roomname>/users/", views.ConnectedUsers.as_view()),
]
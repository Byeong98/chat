from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomList.as_view()),
    path("<str:roomname>/", views.ConnectedUsers.as_view()),
]
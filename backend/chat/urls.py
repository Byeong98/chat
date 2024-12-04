from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomCreateAPIView.as_view()),
    path("list/", views.ChatRoomListAPIView.as_view()),
    path("rank/", views.ChatRoomRankAPIView.as_view()),
    # path("<str:room_id>/users/", views.ConnectedUsersAPIView.as_view()),
]
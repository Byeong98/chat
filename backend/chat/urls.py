from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChatRoomList.as_view()),
]
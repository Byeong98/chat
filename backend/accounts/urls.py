from django.urls import path

from . import views

urlpatterns = [
    path("singup/", views.AccountsAPIView.as_view()),
]
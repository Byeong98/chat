from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.AccountsAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("logout/", views.LogoutAPIView.as_view()),
    path("logged/", views.get_logged_in_usersAPIView.as_view()),
]
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.AccountsAPIView.as_view()),
    path("login/", views.Login_View.as_view()),
    path("logged/", views.get_logged_in_users.as_view()),
    # path("alllogin/", views.all_users_login),
]
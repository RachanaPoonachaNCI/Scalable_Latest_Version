from django.urls import path, re_path
from . import views

urlpatterns = [
    path("login/", views.login_api),
    path("signup/", views.signup_api),
    path("logout/", views.logout_api),
    path("", views.authentication),
]

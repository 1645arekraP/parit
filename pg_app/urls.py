from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/profile/", views.profile, name="home"),
    path("group/<str:invite_code>/", views.group, name="group"),
    path("group/settings/<str:invite_code>/", views.groupSettings, name="groupSettings"),
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account/register/", views.register, name="register"),
    path("account/login/", views.login, name="login"),
    path("account/update-solution/<str:username>/", views.update_solution, name="solution_check"),
    path("account/profile/", views.profile, name="home"),
    path("group/<str:invite_code>/", views.group, name="group"),
]
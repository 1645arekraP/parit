from django.urls import path

from . import views

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
    #path("account/register/", views.register, name="register"),
    #path("account/login/", views.login, name="login"),
    #path("account/profile/", views.profile, name="home"),
    #path("group/<str:invite_code>/", views.group, name="group"),
    #path("group/<str:invite_code>/refresh/", views.refresh_group_data, name="refresh_group_data"),
    #path("<str:username>/solution/<str:question_slug>/", views.solution, name="solution")
]
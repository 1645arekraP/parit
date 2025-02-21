from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/update-group-solutions/<str:group_id>/", views.update_group_solutions, name="solution_check"),
    path("accounts/profile/", views.profile, name="home"),
    path("group/<str:invite_code>/", views.group, name="group"),
    path("accounts/logout/", views.logout_view, name="logout"),
]
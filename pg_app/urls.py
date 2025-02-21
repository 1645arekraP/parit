from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/update-group-solutions/<str:group_id>/", views.update_group_solutions, name="solution_check"),
    path("accounts/profile/", views.profile, name="profile"),
    path("group/<str:invite_code>/", views.group, name="group"),
    path("accounts/logout/", views.logout_view, name="logout"),
    #path("account/send-friend-request/", views.send_friend_request, name="send_friend_request"),
    path("account/respond-friend-request/<int:request_id>/<str:response>/", views.respond_friend_request, name="respond_friend_request"),
]
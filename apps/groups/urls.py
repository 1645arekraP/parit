from django.urls import path
from . import views

urlpatterns = [
    path("<str:invite_code>/", views.group, name="group"),
    path("<str:invite_code>/refresh/", views.refresh_group_data, name="refresh_group_data"),
    path("<str:invite_code>/settings/", views.group_settings, name="group_settings"),
    path("<str:invite_code>/delete/", views.delete_group, name="delete_group"),
    path("<str:invite_code>/leave/", views.leave_group, name="leave_group"),
    path("<str:invite_code>/save_solution/", views.save_solution, name="save_solution"),
]
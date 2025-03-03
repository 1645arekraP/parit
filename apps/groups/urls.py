from django.urls import path
from . import views

urlpatterns = [
    path("<str:invite_code>/", views.group, name="group"),
    path("<str:invite_code>/refresh/", views.refresh_group_data, name="refresh_group_data"),
]
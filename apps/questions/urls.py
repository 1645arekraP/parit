from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/solution/<str:question_slug>/", views.update_question_solution, name="update_question_solution"),
]
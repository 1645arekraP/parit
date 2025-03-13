from django.shortcuts import render # , redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

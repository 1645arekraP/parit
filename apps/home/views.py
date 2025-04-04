from django.shortcuts import render # , redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        # If the user is authenticated, redirect to the dashboard or another page
        return redirect('profile')
    return render(request, "home.html")

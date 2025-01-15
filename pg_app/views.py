from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm, GroupSettingsForm
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from .models import UserGroup
from .utils.utils import QuestionUtils

def index(request):
    return HttpResponse("Hello, world!")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form was valid!")
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            print(email, password)
            # TODO: Handle logic for if a user doesnt exist. Not sure if this should go here or in the form
            user = authenticate(email=email, password=password)
            if user is not None:
                dlogin(request, user)
                return redirect("/accounts/profile/") #TODO: Bugged and will not work
            else:
                print(user)
                print("Wrong email or password")
        else:
            pass
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@login_required()
def profile(request):
    user = request.user
    return render(request, "profile.html", {"user": user})

@login_required()
def group(request, invite_code):
    user = request.user
    group = UserGroup.userBelongsToGroup(user, invite_code)
    q_utils = QuestionUtils()
    if group:
        return render(request, "group.html", {"user": user, "group": group})
    return HttpResponse("Either this group does not exist or you are not in it!")

@login_required()
def groupSettings(request, invite_code):
    user = request.user
    group = get_object_or_404(UserGroup, invite_code=invite_code)
    if request.method == "POST":
        form = GroupSettingsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect(request.referer)
        else:
            pass
    else:
        form = GroupSettingsForm(instance=group)
    return render(request, "group_settings.html", {"user": user, "group": group, "form": form})


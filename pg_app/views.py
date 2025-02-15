from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm, GroupSettingsForm
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from .models import UserGroup, Profile, Solution
from .utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import json

def index(request):
    return render(request, "index.html")

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
    numberOfExcelledQuestions = user.profile.questions.filter(questionrelation__relation_type="excelled").count()
    numberOfStruggledQuestions = user.profile.questions.filter(questionrelation__relation_type="struggled").count()
    return render(request, "profile.html", {"user": user, "numberOfExcelledQuestions": numberOfExcelledQuestions, "numberOfStruggledQuestions": numberOfStruggledQuestions })


@login_required()
def group(request, invite_code):
    user = request.user
    group = UserGroup.userBelongsToGroup(user, invite_code)
    if group:
        print("group valid!")
        if request.method == "POST":
            print("Method was post!")
            form = GroupSettingsForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                print("Saved!")
                return render(request, "group.html", {"user": user, "group": group, "form": form}) 
            else:
                print("Error!")
                pass
        else:
            form = GroupSettingsForm(instance=group)
        return render(request, "group.html", {"user": user, "group": group, "form": form})
    return HttpResponse("Either this group does not exist or you are not in it!")

@login_required()
async def update_group_solutions(request, group_id):
    if request.method == "POST":
        try:
            question_slug = json.loads(request.body)['question_slug']
            user = request.user
            username = await sync_to_async(lambda: user.username)()
            lc_wrapper = LeetcodeWrapper()
            solutions = await lc_wrapper.get_all_solutions(username, limit=5)
            for solution in solutions:
                if solution['titleSlug'] == question_slug:
                    pass
            return JsonResponse({"message": "Update successful", "Response": solutions})
        except Exception as e:
            #print(e)
            return JsonResponse({"error": "Invalid request"}, status=400)
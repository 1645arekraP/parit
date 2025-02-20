from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm, GroupSettingsForm
from django.contrib.auth import authenticate, login as dlogin
from django.contrib.auth.decorators import login_required
from .models import UserGroup, Profile, Solution, Question
from .utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.http import HttpResponseRedirect
from .utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from django.db import IntegrityError
import asyncio
import json

#TODO: Use reverse method and switch to class based views

def coming_soon(request):
    return render(request, "coming_soon.html")

def index(request):
    return render(request, "index.html")

def register(request):
    #TODO: Cleanup
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
    #TODO: This can be cleaned up
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
    if not group:
        return HttpResponse("Either this group does not exist or you are not in it!", status=404)

    form = GroupSettingsForm(request.POST or None, instance=group)
    group_data = group.get_member_solutions()
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("group", invite_code=invite_code) 
    
    return render(request, "group.html", {"user": user, "group": group, "group_data": group_data, "form": form})

@login_required
def refresh_group_data(request, invite_code):
    print("starting")
    user = request.user
    group = UserGroup.userBelongsToGroup(user, invite_code)
    if not group:
        return HttpResponse("Either this group does not exist or you are not in it!", status=404)
    
    if request.method != "GET":
        return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': solutions})

    lcw = LeetcodeWrapper()
    group = UserGroup.objects.get(invite_code=invite_code)
    question = group.question
    profile = request.user.profile
    for member in group.members.all():
        solutions = asyncio.run(lcw.get_recent_solutions(member.username, 5))
        # TODO: Theres prob a better way of doing this like using a hashmap.
        for solution in solutions.solutions:
            if solution.title_slug == question.title_slug:
                 Solution.create_from_leetcode(question, profile, solution) # This can be switched to update
    group_data = group.get_member_solutions()
    print("returning")
    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': group_data})

@login_required
def solution(request, username, question_slug):
    if request.method == "GET":
        profile = Profile.objects.get(user__username=username)
        question = Question.objects.get(title_slug=question_slug)
        solution = Solution.objects.get(profile=profile, question=question)
        return render(request, 'partials/solution_modal.html', {'solution': solution, 'username': username})
    return JsonResponse({'Status': 'Failed!'})
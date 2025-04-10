from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import GroupSettingsForm
from .models import StudyGroup
from apps.questions.models import Solution
from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from .decorators import owner_required, admin_required, belongs_to_group
from .services.group_service import leave_group as service_leave_group
from apps.questions.services.solution_services import update_solution_from_leetcode
import asyncio
import json

@belongs_to_group
def group(request, invite_code):
    user = request.user
    group = StudyGroup.objects.get(invite_code=invite_code)
    
    solution, created = Solution.objects.get_or_create(user=user, question=group.question)

    form = GroupSettingsForm(request.POST or None, instance=group)
    group_data = group.get_member_solutions()
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("group", invite_code=invite_code) 
    
    return render(request, "group.html", {"user": user, "group": group, "group_data": group_data, "group_settings_form": form, "solution": solution})

@belongs_to_group
def refresh_group_data(request, invite_code):
    print("Refreshing group data")
    user = request.user
    group = StudyGroup.objects.get(invite_code=invite_code)
    
    #if request.method != "GET":
    #    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': solutions})
    
    for member in group.members.all():
        update_solution_from_leetcode(member, group.question.title_slug)
    group_data = group.get_member_solutions()
    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': group_data})

@admin_required
def group_settings(request, invite_code):
    print("Group settings")
    group = StudyGroup.objects.get(invite_code=invite_code)
    return render(request, 'partials/group_settings.html', {'group': group})
    
@belongs_to_group
def leave_group(request, invite_code):
    group = StudyGroup.objects.get(invite_code=invite_code)
    service_leave_group(group, request.user)
    return redirect("profile")

@belongs_to_group
def save_solution(request, invite_code):
    content = request.POST.get('content')
    group = StudyGroup.objects.get(invite_code=invite_code)
    solution = Solution.objects.get(user=request.user, question=group.question)
    solution.code = content
    solution.save()
    return render(request, 'partials/test.html', {'solution': solution})


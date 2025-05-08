from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import GroupEditForm
from .models import StudyGroup, StudyGroupMembership
from apps.questions.models import Solution
from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from .decorators import owner_required, admin_required, belongs_to_group
from .services.group_service import leave_group as service_leave_group, update_group
from apps.questions.services.solution_services import update_from_leetcode, get_or_init
from django.contrib import messages
import json

@belongs_to_group
def group(request, invite_code):
    user = request.user
    group = StudyGroup.objects.get(invite_code=invite_code)
    memberships = group.memberships.all()
    
    solution, created = get_or_init(user=user, question=group.question)

    form = GroupEditForm(request.POST or None, group=group, memberships=memberships)
    group_data = group.get_member_solutions()
    
    if request.method == "POST":
        if form.is_valid():
            update_group(group, form.cleaned_data)
            messages.success(request, 'Updated group settings!')
        else:
            messages.error(request, 'Failed to update group settings!')
        return redirect("group", invite_code=invite_code) 
    
    return render(request, "group.html", {"user": user, "group": group, "group_data": group_data, "group_settings_form": form, "solution": solution, "memberships": memberships})

@belongs_to_group
def refresh_group_data(request, invite_code):
    print("Refreshing group data")
    user = request.user
    group = StudyGroup.objects.get(invite_code=invite_code)
    
    #if request.method != "GET":
    #    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': solutions})
    
    for member in group.members.all():
        update_from_leetcode(member, group.question.title_slug)
    group_data = group.get_member_solutions()
    messages.success(request, 'Group solutions updated!')
    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': group_data})

@belongs_to_group
def leave_group(request, invite_code):
    group = StudyGroup.objects.get(invite_code=invite_code)
    service_leave_group(group, request.user)
    messages.info(request, 'Left group!')
    messages.success(request, 'Left group!')
    return redirect("profile")

@belongs_to_group
def save_solution(request, invite_code):
    content = request.POST.get('content')
    group = StudyGroup.objects.get(invite_code=invite_code)
    solution = Solution.objects.get(user=request.user, question=group.question)
    solution.code = content
    solution.save()
    return render(request, 'partials/test.html', {'solution': solution})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import GroupSettingsForm
from .models import StudyGroup
from apps.questions.models import Solution
from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from .decorators import owner_required, admin_required, belongs_to_group
from .services.group_service import leave_group as service_leave_group, update_solution_code
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
    
    return render(request, "group.html", {"user": user, "group": group, "group_data": group_data, "form": form, "solution": solution})

@belongs_to_group
def refresh_group_data(request, invite_code):
    print("Refreshing group data")
    user = request.user
    group = StudyGroup.objects.get(invite_code=invite_code)
    
    if request.method != "GET":
        return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': solutions})

    lcw = LeetcodeWrapper()
    group = StudyGroup.objects.get(invite_code=invite_code)
    question = group.question
    for member in group.members.all():
        print(member.leetcode_username)
        solutions = asyncio.run(lcw.get_recent_solutions(member.leetcode_username))
        print(solutions)
        for solution in solutions.solutions:
            print(solution.title_slug)
            if solution.title_slug == question.title_slug:
                 print("Found solution")
                 Solution.create_from_leetcode(question, user, solution) # This can be switched to update
    group_data = group.get_member_solutions()
    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': group_data})

@admin_required
def group_settings(request, invite_code):
    group = StudyGroup.objects.get(invite_code=invite_code)
    return render(request, 'partials/group_settings.html', {'group': group})

@owner_required
def delete_group(request, invite_code):
    #TODO: This gotta be validated
    group = StudyGroup.objects.get(invite_code=invite_code)
    try:
        group.delete()
        return redirect("profile")
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@belongs_to_group
def leave_group(request, invite_code):
    group = StudyGroup.objects.get(invite_code=invite_code)
    service_leave_group(group, request.user)
    return redirect("profile")

@belongs_to_group
def save_solution(request, invite_code):
    content = request.POST.get('content')
    group = StudyGroup.objects.get(invite_code=invite_code)
    update_solution_code(group, request.user, content)
    return render(request, 'partials/test.html')

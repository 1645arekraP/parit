from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import GroupSettingsForm
from .models import StudyGroup
from apps.questions.models import Solution
from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
import asyncio

@login_required()
def group(request, invite_code):
    user = request.user
    group = StudyGroup.userBelongsToGroup(user, invite_code)
    if not group:
        return HttpResponse("Either this group does not exist or you are not in it!", status=404)

    form = GroupSettingsForm(request.POST or None, instance=group)
    group_data = group.get_member_solutions()
    print(group_data)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("group", invite_code=invite_code) 
    
    return render(request, "group.html", {"user": user, "group": group, "group_data": group_data, "form": form})

@login_required
def refresh_group_data(request, invite_code):
    user = request.user
    group = StudyGroup.userBelongsToGroup(user, invite_code)
    if not group:
        return HttpResponse("Either this group does not exist or you are not in it!", status=404)
    
    if request.method != "GET":
        return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': solutions})

    lcw = LeetcodeWrapper()
    group = StudyGroup.objects.get(invite_code=invite_code)
    question = group.question
    for member in group.members.all():
        solutions = asyncio.run(lcw.get_recent_solutions(member.leetcode_username, 5))
        # TODO: prob a better way of doing this
        for solution in solutions.solutions:
            if solution.title_slug == question.title_slug:
                 Solution.create_from_leetcode(question, user, solution) # This can be switched to update
    group_data = group.get_member_solutions()
    return render(request, 'partials/members_table.html', {'group': group, 'user':user, 'group_data': group_data})
from apps.accounts.models import CustomUser
from apps.questions.models import Question, Solution
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from apps.groups.decorators import belongs_to_group
from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper


@login_required
def update_question_solution(request, question_slug, username):
    """
    This should update the solution for a question using the leetcode wrapper.
    """
    print("Updating solution")
    if request.method == "GET":
        user = CustomUser.objects.get(username=username)
        question = Question.objects.get(title_slug=question_slug)
        solution = Solution.objects.get(user=user, question=question)
        
    return render(request, 'partials/solution_modal.html', {'solution': solution, 'username': user.username})
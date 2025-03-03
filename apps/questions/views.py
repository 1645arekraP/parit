from apps.accounts.models import CustomUser
from apps.questions.models import Question, Solution
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def solution(request, username, question_slug):
    if request.method == "GET":
        user = request.user
        question = Question.objects.get(title_slug=question_slug)
        solution = Solution.objects.get(user=user, question=question)
        return render(request, 'partials/solution_modal.html', {'solution': solution, 'username': username})
    return JsonResponse({'Status': 'Failed!'})
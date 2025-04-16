from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from apps.questions.models import Question, Solution
from django.http import JsonResponse
from django.db import transaction
import asyncio

def get_or_init(user, question):
    # returns solution, created
    with transaction.atomic():
        try:
            solution = Solution.objects.select_for_update().get(user=user, question=question)
            return solution, False
        except Solution.DoesNotExist:
            solution = Solution.objects.create(user=user, question=question)
            return solution, True

def update_solution_model(user, question, leetcode_solution):
    """
    This should update a solution object for a user and question from leetcode
    """
    with transaction.atomic():
        solution, created = get_or_init(user=user, question=question)

        # Old solution, don't update
        if float(leetcode_solution.timestamp) <= float(solution.last_updated):
            return solution
        
        status = 'solved' if leetcode_solution.status == 'Accepted' else 'in_progress'
        fields_to_update = {
            'attempts': solution.attempts + 1,
            'memory': leetcode_solution.memory,
            'runtime': leetcode_solution.runtime,
            'last_updated': leetcode_solution.timestamp,
            'status': status
        }
        for field, value in fields_to_update.items():
            setattr(solution, field, value)
        solution.save()
        return solution
    
def update_from_leetcode(user, question_slug):
    #if user.last_solution_update > timezone.now() - timedelta(minutes=1):
        # TODO: Throw an error hint or something
    #    print("too soon!")
    #    return

    leetcode_wrapper = LeetcodeWrapper()
    question = Question.objects.get(title_slug=question_slug)
    leetcode_solutions = asyncio.run(leetcode_wrapper.get_recent_solutions(user.leetcode_username, 15)).solutions
    
    for solution in leetcode_solutions:
        try:
            if solution.title_slug == question_slug:
                update_solution_model(user=user, question=question, leetcode_solution=solution)
        except Exception as e:
            print(e)
    return JsonResponse({'Status': 'Success!'})

def update_solution_code(group, user, code):
    """
    This should update the code of a solution object for a user and question
    """
    question = group.question
    solution = Solution.objects.get(question=question, user=user)
    solution.code = code
    solution.save()
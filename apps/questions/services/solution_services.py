from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from apps.questions.models import Question, Solution
from django.http import JsonResponse
import asyncio

def create_solution(question, user):
    """
    This should create a solution object for a user and question.
    If a solution already exists, it should not be created again but instead tagged as a duplicate
    """
    solution, created = Solution.objects.get_or_create(question=question, user=user)


def update_solution_from_leetcode(user, question):
    """
    This should update a solution object for a user and question from leetcode
    """
    question_slug = question.title_slug
    leetcode_wrapper = LeetcodeWrapper()
    leetcode_solutions = asyncio.run(leetcode_wrapper.get_recent_solutions(user.leetcode_username, 15)).solutions
    for solution in leetcode_solutions:
        if solution.title_slug == question_slug:
            # This creates a solution object if it doesn't exist but also checks to see if the solution is the latest
            # This should be ok for now, but eventually we should check if the solution is the latest and break out earlier in the loop
            # TODO: Modify wrapper to return a hashmap of question_slug -> solution
            Solution.create_from_leetcode(question, user, solution)
    return JsonResponse({'Status': 'Success!'})

def update_solution_code(group, user, code):
    """
    This should update the code of a solution object for a user and question
    """
    question = group.question
    solution = Solution.objects.get(question=question, user=user)
    solution.code = code
    solution.save()

"""def update_solution(user, question):
    leetcode_wrapper = LeetcodeWrapper()
    _, leetcode_solutions = asyncio.run(leetcode_wrapper.get_recent_solutions(user.leetcode_username, 15))
    for solution in leetcode_solutions:
        if solution.title_slug == question.title_slug:
        solution = Solution.get_or_create(question, user, solution)"""
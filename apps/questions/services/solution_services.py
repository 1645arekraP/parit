from apps.questions.utils.wrappers.leetcode.leetcode_wrapper import LeetcodeWrapper
from apps.questions.models import Question, Solution
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
    pass

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
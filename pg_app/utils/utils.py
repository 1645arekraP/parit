from .LeetcodeWrapper import LeetcodeWrapper
from ..models import Question
from random import choice

class QuestionUtils():
    def __init__(self):
        self.leetcode_wrapper = LeetcodeWrapper()

    def __getDailyQuestion(self):
        return self.leetcode_wrapper.getDailyQuestion()
    
    def getQuestion(self, category):
        if category == "DAILY":
            return self.__getDailyQuestion()
        try:
            questions = Question.objects.filter(pool_tag__contains=category)
            question = choice(questions)
            return question
        except Exception as e :
            print(f"Exception: {e}")
        return None
        
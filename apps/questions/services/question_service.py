from apps.questions.models import Question
import random

# TODO: Create a filter using Django's filter class
def get_new_question(study_set):
    questions = list(Question.objects.filter(pool_tag__contains=study_set))
    if questions:
        question = random.choice(questions)
    else:
        question = Question.objects.first()
    return question
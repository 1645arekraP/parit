from .models import UserGroup, Question

# TODO: Swap to Celery

def update_daily_question():
    for group in UserGroup.objects.all():
        group.update_daily_question()

def update_questions():
    pass
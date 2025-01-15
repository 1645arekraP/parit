from .models import UserGroup, Question

def update_daily_question():
    print("Job went off!")
    for group in UserGroup.objects.all():
        group.update_daily_question()

def update_questions():
    pass
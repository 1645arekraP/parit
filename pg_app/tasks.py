from .models import UserGroup, Question, Profile

# TODO: Swap to Celery

def update_daily_question():
    for group in UserGroup.objects.all():
        group.update_daily_question()

def update_questions():
    pass

def update_daily_streak():
    print("Updating Streak")
    for profile in Profile.objects.all():
        profile.update_streak()
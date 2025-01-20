from .models import UserGroup, Question, Profile

def update_daily_question():
    print("Job went off!")
    for group in UserGroup.objects.all():
        group.update_daily_question()

def update_questions():
    pass

def update_daily_streak():
    print("Updating Streak")
    for profile in Profile.objects.all():
        profile.update_streak()
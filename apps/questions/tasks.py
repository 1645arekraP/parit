from celery import shared_task
from datetime import datetime
from apps.questions.services.solution_services import update_solution
from apps.accounts.models import CustomUser

@shared_task(name='questions.tasks.test_task')
def test_task():
    user = CustomUser.objects.get(username="parker")
    update_solution(user, "two-sum")
    print("Solution updated")
    return "Hello, world!"

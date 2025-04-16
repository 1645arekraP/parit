from celery import shared_task
from datetime import datetime
from apps.questions.services.solution_services import update_from_leetcode
from apps.accounts.models import CustomUser
from apps.questions.models import Question
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.groups.models import StudyGroup
from apps.questions.models import Solution
from django.template.loader import get_template
from django.core.cache import cache
from django_redis import get_redis_connection
from apps.questions.services.solution_services import get_random_question

@shared_task(name='questions.tasks.update_group_solutions_tasks')
def update_group_solutions_tasks():

    redis = get_redis_connection()
    groups = redis.hkeys("active_groups")
    print(f"Groups: {groups}")
    for invite_code in groups:
        print(f"Invite code: {invite_code}")
        group = StudyGroup.objects.get(invite_code=invite_code)
        question = group.question
        print(f"Updating group: {group.group_name} - {group.invite_code}")
        for member in group.members.all():
            update_from_leetcode(member, question.title_slug)

            # Get group data TODO: A view already has this logic so we should move it to a service
            group_data = group.get_member_solutions()

            # Format group data for websocket
            html = get_template("partials/members_table.html").render(
                    context={
                        "group_data": group_data,
                        "group": group
                    }
                )

            # Send message to websocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group.invite_code,
                {
                    "type": "updated_solutions",  # Must match your consumer method name
                    "html": html
                }
            )

@shared_task(name='questions.tasks.update_group_quesions_tasks')
def update_group_quesions_tasks():
    #TODO: We should also be checking if the question is already in the group
    #TODO: We should also save the solutions to previous questions before updating the question
    redis = get_redis_connection()
    groups = redis.hkeys("active_groups")
    for invite_code in groups:
        group = StudyGroup.objects.get(invite_code=invite_code)
        question = group.question
        print(f"Updating group: {group.group_name} - {group.invite_code}")
        question = get_random_question()
        group.question = question
        group.save()
        print(f"Updated group: {group.group_name} - {group.invite_code}")

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group.invite_code,
            {
                "type": "updated_question",  # Must match your consumer method name,
                "status": "success" # TODO: Add status
            }
        )

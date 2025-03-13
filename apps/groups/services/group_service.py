from apps.groups.models import StudyGroup, StudyGroupMembership
from apps.questions.models import Question, Solution
from apps.questions.services.solution_services import create_solution

def create_group(user, group_name, question_pool_type, initial_members=None):
    question = Question.objects.all()[0] # This should be a random question
    invite_code = StudyGroup.create_unique_invite_code()    
    group = StudyGroup.objects.create(
        group_name=group_name,
        question_pool_type=question_pool_type,
        invite_code=invite_code,
        question=question
    )
    # Give the creator admin role
    group.members.add(user)
    group.update_member_role(user, "ADMIN")
    # Add initial members
    if initial_members:
        group.members.add(*initial_members)
    # Create a solution for each initial member
    for member in initial_members:
        create_solution(question, member)
    return group

def update_role(group, user, role):
    group.update_member_role(user, role)


def leave_group(group, user):
    if group.members.count() == 1:
        group.delete()
    else:
        group.members.remove(user)
        if group.members.count() == 1 and group.members.first().role == "MEMBER":
            group.update_member_role(group.members.first(), "ADMIN")

def update_group_question(group):
    """
    This function will be called daily to update the group's question
    """
    group.question = Question.objects.all()[0] # Change this to be a random question
    # Update the question for each member
    for member in group.members.all():
        solution = create_solution(group.question, member)
    group.save()
import shortuuid
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from typing import Dict, Self
from ..questions.models import Question, Solution
from ..accounts.models import CustomUser
from django.core.exceptions import ValidationError

class StudyGroup(models.Model):
    """
    Model representing a study group.
    """
    QUESTION_POOL_TYPE_CHOICES = [
        ("DAILY", "Daily Question"),
        ("BLIND_75", "Blind 75"),
        ("NEETCODE_150", "Neetcode 150"),
        ("NEETCODE_250", "Neetcode 250"),
        ("LC_ALL", "Leetcode All"),
    ]

    PRIVACY_CHOICES = [
        ("INVITE_ONLY", "Invite Only"),
        ("FRIENDS_ONLY", "Friends Only"),
        ("PUBLIC", "Public"),
    ]
    
    members = models.ManyToManyField(CustomUser, related_name="study_groups", through="StudyGroupMembership")
    question = models.ForeignKey(
        Question, 
        on_delete=models.SET_NULL, #TODO: Look into this and the best way to handl deletion 
        null=True, 
        blank=True, 
        default=None,
        related_name="study_groups", 
    )
    invite_code = ShortUUIDField(
        unique=True,
        length=8,
        editable=False
    )
    group_name = models.CharField(
        max_length=254,
        unique=False, 
        blank=False, 
        null=False, 
        default="Unnamed Group"
    )
    question_pool_type = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        default="DAILY",
        choices=QUESTION_POOL_TYPE_CHOICES
    )
    privacy = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        default="PRIVATE",
        choices=PRIVACY_CHOICES
    )
    
    # Move this to a service
    def update_daily_question(self):
        # TODO: This should be in a service
        self.question = self.question.get_new_question(self.question_pool_type)
        self.save()
    # Move this to a service
    def get_member_solutions(self) -> Dict:
        # TODO: This should be in a service
        solutions = []
        for member in self.members.all():
            solution, _ = Solution.objects.get_or_create(
                question=self.question,
                user=member,
                defaults={
                    'status': 'Not Started'
                }
            )
            solutions.append((member, solution))
        return solutions

    
    
    @classmethod
    def create_unique_invite_code(cls):
        attempts = 0
        invite_code = shortuuid.ShortUUID().random(length=8)
        while cls.objects.filter(invite_code=invite_code).exists():
            invite_code = shortuuid.ShortUUID().random(length=8)
            attempts += 1
            if attempts > 10:
                raise ValueError("Failed to create a unique invite code")
        return invite_code
    
    @classmethod
    def join_group(cls, user, invite_code):
        """
        Class method to join a group using an invite code
        """
        group = cls.objects.get(invite_code=invite_code)
        group.members.add(user)
        return group

    # Move this to a service
    def update_member_role(self, target_user, new_role):
        """
        Update a member's role
        Args:
            target_user: The user whose role is being changed
            new_role: The new role to assign
        """
        target_membership = StudyGroupMembership.objects.filter(
            study_group=self,
            user=target_user
        ).first()

        if not target_membership:
            raise ValidationError("User must be a member of the group")

        target_membership.role = new_role
        target_membership.save()

class StudyGroupMembership(models.Model):
    ROLES = [
        ("ADMIN", "Admin"), 
        ("MEMBER", "Member"),
    ]
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default="MEMBER")

    class Meta:
        unique_together = ('study_group', 'user')

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.study_group.group_name}"
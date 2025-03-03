import shortuuid
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from typing import Dict, Self
from ..questions.models import Question, Solution
from ..accounts.models import CustomUser

class StudyGroup(models.Model):
    """
    Model representing a study group.
    """
    members = models.ManyToManyField(CustomUser, related_name="study_groups")
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
        choices=[
        ("DAILY", "Daily Question"),
        ("BLIND_75", "Blind 75"),
        ("NEETCODE_150", "Neetcode 150"),
        ("NEETCODE_250", "Neetcode 250"),
        ("LC_ALL", "Leetcode All"),
        ("CUSTOM", "Custom Pool"),
        ]
    )

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = shortuuid.ShortUUID().random(length=8)
        
        # Hacked together solution. TODO: Find a better way to do this
        #self.question = Question.get_new_question(self.question_pool_type)
        #self.question = Question.objects.all()[0]

        while True:
            try:
                with transaction.atomic():
                    super().save(*args, **kwargs)
                    break
            except IntegrityError:
                self.invite_code = shortuuid.ShortUUID().random(length=8)
                continue
    
    def update_daily_question(self):
        self.question = self.question.get_new_question(self.question_pool_type)
        self.save()

    def get_member_solutions(self) -> Dict:
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
    
    @staticmethod
    def userBelongsToGroup(user, group_id) -> Self:
        """
        Method to validate if a user is in the group they are trying to join. 
        Returns the group object if they are in the group and returns None if they are not.
        """
        try:
            group = user.study_groups.get(invite_code=group_id)
            return group
        except StudyGroup.DoesNotExist:
            return None
    
    def __str__(self):
        return self.invite_code
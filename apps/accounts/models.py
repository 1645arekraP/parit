from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    # Basic user info
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), blank=False)
    friends = models.ManyToManyField("self", blank=True, symmetrical=True)

    # Leetcode 
    leetcode_username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text='Your LeetCode username',
        validators=[UnicodeUsernameValidator()], # TODO: Add a custom validator
        error_messages={
            'unique': 'This LeetCode username is already taken.',
        },
    )

    # User stats
    acceptance_rate = models.FloatField(default=0.0)
    streak = models.IntegerField(default=0)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    questions = models.ManyToManyField("questions.Question", through="questions.QuestionRelation")

    @classmethod
    def update_streak(self):
        currentDate = timezone.now()
        yesterday = currentDate - timedelta(days = 1)

        recent_solution = self.solutions.filter(
            date=yesterday,
            accepted=True  # Only count accepted solutions
        ).exists()

        if not recent_solution:
            self.streak = 0
        
        self.save()
        return


    @classmethod
    def calculate_acceptance_rate(self):
        numberOfSolutions = self.solutions.count()
        if numberOfSolutions == 0:
            return 0
        
        numAcceptedSolution = self.solutions.filter(accepted=True).count()
        return (numAcceptedSolution/numberOfSolutions) * 100
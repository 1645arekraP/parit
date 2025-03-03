import random
from django.db import models
from django.utils.translation import gettext_lazy as _

class Question(models.Model):
    topic_tags = models.JSONField(null=True, blank=True)
    ac_rate = models.FloatField()
    content = models.CharField(null=True, blank=True, max_length=5012)
    difficulty = models.CharField(max_length=1024)
    is_paid = models.BooleanField(default=False)
    link = models.URLField()
    title = models.CharField(max_length=1024)
    title_slug = models.SlugField(unique=True, null=False, blank=False, max_length=255)
    pool_tag = models.JSONField(default=list)

    @classmethod
    def get_new_question(cls, category):
        #TODO: REFACTOR
        question = None
        try:
            questions = cls.objects.filter(pool_tag__contains=category)
            question = random.choice(list(questions))
        except Exception as e :
            print(f"Exception: {e}")
        return question

    def __str__(self):
        return self.title_slug
    
class Solution(models.Model):
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, default="two-sum", related_name="solution")
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name='solution',
    )
    STATUS_CHOICES = [
        ('has_not_started', _('Has not started')),
        ('in_progress', _('In progress')),
        ('solved', _('Solved'))
    ]
    memory = models.CharField(default=-1, blank=True, max_length=12)
    runtime = models.CharField(default=-1, blank=True, max_length=12)
    status = models.CharField(choices=STATUS_CHOICES, default='has_not_started', max_length=28)
    last_updated = models.CharField(default=str(float('inf')), max_length=250)
    attempts = models.IntegerField(default=0)

    @classmethod
    def create_from_leetcode(cls, question, user, solution_object):
        #TODO: Find a better way of setting this
        choice = 'In Progress'
        if solution_object.status=='Accepted':
            choice = 'Accepted'

        defaults = {
            'memory': solution_object.memory,
            'runtime': solution_object.runtime,
            'last_updated': solution_object.timestamp,
            'status': choice
        }
        
        return cls.objects.update_or_create(
            question=question,
            user=user,
            defaults=defaults
        )

    class Meta:
        unique_together = ("user", "question")

class QuestionRelation(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    relation_type = models.CharField(
        max_length=20,
        choices=[
            ("solved", "Solved"),
            ("excelled", "Excelled"),
            ("struggled", "Struggled"),
            ("unsolved", "Unsolved"),
            ("strugglingToSolve", "StrugglingToSolve"),
        ],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question", "relation_type")


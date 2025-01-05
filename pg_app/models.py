from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        
        if not username:
            raise ValueError(_("The Username field must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, username, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that has a unique email rather than username.
    """
    email = models.EmailField(
        primary_key=True,
        blank=False,
        null=False,
        unique=True,
        max_length=254
    )

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=36,
        blank=False,
        null=False,
        validators=[username_validator]
    )
    groups=models.ManyToManyField("UserGroup")
    
    is_staff = models.BooleanField(
        default=False
    )

    is_superuser = models.BooleanField(
        default=False
    )

    #TODO: implement logic
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(
        default=now
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserGroup(models.Model):
    """
    Model representing a grpoup.
    """

    question_pool_types = [
        
    ]

    id = models.CharField(
        primary_key=True,
        blank=False,
        unique=True,
        max_length=12,
    )
    group_name = models.CharField(
        max_length=254
    )
    members = models.ManyToManyField("User")

    question_pool_type = models.CharField(
        max_length=36,
        default="daily"
    ) # This is if users want to pool questions from all lc questions, daily question, blind 75, neetcode 150, or a custom pool

class Profile(models.Model):
    """
    Model representing a profile. This keeps track of the user's stats across multiple sources. 
    """

    user = models.OneToOneField(
        "User",
        primary_key=True,
        on_delete=models.CASCADE,
    )

class Solution(models.Model):
    """
    Model representing a user's latest submission.
    """
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=254
    )
    question_id = models.IntegerField(
        primary_key=True,
        blank=False,
        unique=True
    )
    memory = models.FloatField(

    )
    runtime = models.FloatField(

    )
    tags = models.JSONField(
        # Store as JSON string, prob a better way to do this
    )
    accepted = models.BooleanField(
        default=False
    )
    date = models.DateTimeField(
        
    )
    attempts = models.IntegerField(
        default=0
    )
    # Not sure what the char field for this should be or the max length
    code = models.CharField(
        blank=True,
        max_length=1024
    )


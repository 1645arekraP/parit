import shortuuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from shortuuid.django_fields import ShortUUIDField
from django.db import IntegrityError, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    """
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not username:
            raise ValueError(_("The Username field must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that has a unique email rather than username.
    """
    email = models.EmailField(
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
    user_groups = models.ManyToManyField("UserGroup")

    # Overridden attributes
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # TODO: Implement logic for is_active. This should be changed to false if the user hasn't been active in over a week
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserGroup(models.Model):
    """
    Model representing a group.
    """
    invite_code = ShortUUIDField(
        unique=True,
        length=8,
    )
    group_name = models.CharField(max_length=254, blank=False, null=False, default="Unnamed Group")
    members = models.ManyToManyField("CustomUser")
    question_pool_type = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        default="DAILY",
        choices=[
        ("DAILY", "Daily Question"),
        ("BLIND75", "Blind 75"),
        ("NEETCODE150", "Neetcode 150"),
        ("NEETCODE250", "Neetcode 250"),
        ("ALL", "All"),
        ("CUSTOM", "Custom Pool"),
        ]
    )

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = shortuuid.ShortUUID().random(length=8)

        while True:
            try:
                with transaction.atomic():
                    super().save(*args, **kwargs)
                    break
            except IntegrityError:
                self.invite_code = shortuuid.ShortUUID().random(length=8)
                continue




class Profile(models.Model):
    """
    Model representing a profile. This keeps track of the user's stats across multiple sources. 
    TODO: We need to make sure that when a user deletes their account, 
    that it will ONLY delete the profile if it is only tied to ONE account, otherwise don't delete it
    """
    user = models.OneToOneField(
        "CustomUser",
        primary_key=True,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    # TODO: Keep track of stats to be used for ML / AI purposes

class Solution(models.Model):
    """
    Model representing a user's latest submission.
    """
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    question_slug = models.CharField(
        max_length=36,
        null=False,
        blank=False
    )
    memory = models.FloatField()
    runtime = models.FloatField()
    tags = models.JSONField()
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(default=now)
    attempts = models.IntegerField(default=0)
    # Not sure what the char field for this should be or the max length
    code = models.TextField(blank=True)

    class Meta:
        unique_together = ("profile", "question_slug")
        ordering = ["-date"]
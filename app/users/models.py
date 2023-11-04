import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **additional_fields):
        """Create new user."""
        if not email:
            raise ValueError("A user must have an email.")

        user = self.model(email=self.normalize_email(email), **additional_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **additional_fields):
        """Create new superuser"""
        user = self.create_user(email, password, **additional_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


USER_ROLES_CHOICES = [
    ("Admin", "Admin"),
    ("Participant", "Participant"),
]


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(
        blank=True,
        null=True,
        upload_to="profiles/",
        default="profiles/default_photo.jpg",
    )
    location = models.CharField(max_length=150, blank=True)
    teammates = models.ManyToManyField("User", related_name="teammate", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    skills = models.ManyToManyField("Skill", blank=True)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, max_length=36, unique=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Skill(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

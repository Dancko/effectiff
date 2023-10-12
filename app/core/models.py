from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone

from ckeditor.fields import RichTextField
from django_cryptography.fields import encrypt


now = timezone.now()


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
    ('Admin', 'Admin'),
    ('Participant', 'Participant'),
]


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    teammates = models.ManyToManyField('User', related_name='teammate', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    skills = models.ManyToManyField('Skill', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Project(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField('Category', blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner')
    participants = models.ManyToManyField('User', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('Moderate', 'Moderate'),
        ('Non-Urgent', 'Non-Urgent'),
    ]

    STATUS_CHOICES = [
        ('Awaits', 'Awaits'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Expired', 'Expired')
    ]

    title = models.CharField(max_length=250)
    body = RichTextField(blank=True, null=True)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Non-Urgent')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Awaits')
    category = models.ManyToManyField('Category', blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    outdated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated', '-created']

    def is_outdated(self):
        if self.deadline < now:
            self.outdated = True
            self.save()
        else:
            self.outdated = False
            self.save()
        return self.outdated


class Skill(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, default=None)
    body = encrypt(models.TextField())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-created']

import uuid
import os

from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField


now = timezone.now()


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("Moderate", "Moderate"),
        ("Non-Urgent", "Non-Urgent"),
    ]

    STATUS_CHOICES = [
        ("Awaits", "Awaits"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Expired", "Expired"),
    ]

    title = models.CharField(max_length=250)
    body = HTMLField(blank=True, null=True)
    deadline = models.DateTimeField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="Non-Urgent"
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Awaits")
    category = models.ManyToManyField("projects.Category", blank=True)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="tasks"
    )
    assigned_to = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    outdated = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated", "-created"]

    def is_outdated(self):
        if self.deadline < now:
            self.outdated = True
            self.save()
        else:
            self.outdated = False
            self.save()
        return self.outdated


class TaskFile(models.Model):
    task = models.ForeignKey("Task", related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="tasks_attachments/")

    @property
    def get_ext(self):
        filename = str(self.file.name)
        return filename.split(".")[-1] if "." in filename else None

    @property
    def short_name(self):
        filename = str(self.file.name)
        return filename.split("/")[-1]

    def __str__(self):
        return self.short_name


class Comment(models.Model):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    task = models.ForeignKey(
        "tasks.Task", related_name="comment", on_delete=models.CASCADE, default=None
    )
    body = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["created"]


class CommentFile(models.Model):
    comment = models.ForeignKey(
        "Comment", related_name="files", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="comment_attachments/")

    @property
    def get_ext(self):
        filename = str(self.file.name)
        return filename.split(".")[-1] if "." in filename else None

    @property
    def short_name(self):
        filename = str(self.file.name).split("/")[-1]
        return filename[-20:]

    def __str__(self):
        return self.short_name

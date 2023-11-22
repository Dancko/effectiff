import uuid

from django.db import models

from tinymce.models import HTMLField


class Project(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField("Category", blank=True)
    description = HTMLField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User",
        related_name="projects",
        on_delete=models.CASCADE,
    )
    participants = models.ManyToManyField("users.User", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-updated", "-created"]


class ProjectFile(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    file = models.FileField(upload_to="project_attachments/")

    def __str__(self) -> str:
        return self.project.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

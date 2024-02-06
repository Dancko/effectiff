import uuid

from django.db import models
from django.conf import settings

from tinymce.models import HTMLField


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ManyToManyField("Category", blank=True)
    description = HTMLField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        on_delete=models.CASCADE,
    )
    participants = models.ManyToManyField("users.User", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated", "-created"]


class ProjectFile(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_files"
    )
    file = models.FileField(upload_to="project_attachments/")

    @property
    def short_name(self):
        filename = str(self.file.name).split("/")[-1]
        return filename[-20:]

    @property
    def get_ext(self):
        return self.short_name.split(".")[-1]

    def __str__(self):
        return self.short_name


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

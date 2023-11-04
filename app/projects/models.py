import uuid

from django.db import models

from tinymce.models import HTMLField


class Project(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField("Category", blank=True)
    description = HTMLField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="owner"
    )
    participants = models.ManyToManyField("users.User", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-updated", "-created"]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

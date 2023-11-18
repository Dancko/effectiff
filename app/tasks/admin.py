from django.contrib import admin

from .models import Task, TaskFile, Comment, CommentFile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "assigned_to"]


admin.site.register(Comment)
admin.site.register(TaskFile)
admin.site.register(CommentFile)

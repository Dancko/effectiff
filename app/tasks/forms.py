from django.forms import ModelForm

from core.models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body', 'deadline', 'priority', 'category', 'project', 'assigned_to']

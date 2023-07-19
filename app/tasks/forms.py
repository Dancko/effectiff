from django.forms import ModelForm
from django import forms

from core.models import Task


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body', 'deadline', 'priority', 'category', 'project', 'assigned_to']
        widgets = {'deadline': DateTimeInput()}



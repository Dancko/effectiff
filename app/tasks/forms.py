from django.forms import ModelForm
from django import forms

from core.models import Task, Comment


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'body', 'deadline', 'priority', 'category', 'project']
        widgets = {'deadline': DateTimeInput()}


class TaskAddPartiicipantsForm(ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to']

    def __init__(self, *args, **kwargs):
        super(TaskAddPartiicipantsForm, self).__init__(*args, **kwargs)

        assignee = self.instance.project.owner.teammates.all()
        self.fields['assigned_to'].queryset = assignee


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

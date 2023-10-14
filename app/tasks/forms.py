from django.forms import ModelForm
from django import forms

from core.models import Task, Comment, Project


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TaskCreateForm(ModelForm):
    # body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    

    class Meta:
        model = Task
        fields = ['project', 'title', 'body', 'deadline', 'priority', 'assigned_to']
        widgets = {'deadline': DateTimeInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        teammates = user.teammates.all()
        self.fields['assigned_to'].queryset = teammates
        projects = Project.objects.filter(owner=user)
        self.fields['project'].queryset = projects


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

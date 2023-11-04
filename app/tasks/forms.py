from django.forms import ModelForm
from django import forms

from tasks.models import Task, Comment
from projects.models import Project


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class TaskCreateForm(ModelForm):
    # body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

    class Meta:
        model = Task
        fields = [
            "project",
            "title",
            "body",
            "deadline",
            "priority",
            "assigned_to",
        ]
        widgets = {"deadline": DateTimeInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        teammates = user.teammates.all()
        self.fields["assigned_to"].queryset = teammates
        projects = Project.objects.filter(owner=user)
        self.fields["project"].queryset = projects


class TaskCreateFromProjectForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "body", "deadline", "priority", "assigned_to"]
        widgets = {"deadline": DateTimeInput()}

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super(TaskCreateFromProjectForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        teammates = project.participants.all()
        self.fields["assigned_to"].queryset = teammates


class TaskAddPartiicipantsForm(ModelForm):
    class Meta:
        model = Task
        fields = ["assigned_to"]

    def __init__(self, *args, **kwargs):
        super(TaskAddPartiicipantsForm, self).__init__(*args, **kwargs)

        assignee = self.instance.project.owner.teammates.all()
        self.fields["assigned_to"].queryset = assignee


class CommentForm(ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control rounded-3 form-comment",
                "placeholder": "Enter Your Message Here",
                "rows": "7",
            }
        )
    )

    class Meta:
        model = Comment
        fields = ["body"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields["body"].label = ""

from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from tasks.models import Task, Comment
from projects.models import Project


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, max_files=10, **kwargs):
        self.max_files = max_files
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            if self.max_files and len(data) > self.max_files:
                raise ValidationError(f"Only {self.max_files} files allowed.")
            result = [single_file_clean(d, initial) for d in data]

            if len(result) > self.max_files:
                raise ValidationError(f"Only {self.max_files} files allowed.")
        else:
            result = single_file_clean(data, initial)
        return result


class TaskCreateForm(ModelForm):
    files = MultipleFileField(max_files=10, required=False)

    class Meta:
        model = Task
        fields = [
            "project",
            "title",
            "body",
            "deadline",
            "priority",
            "assigned_to",
            "files",
        ]
        widgets = {"deadline": DateTimeInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        files_dict = kwargs.pop("files", {})

        super(TaskCreateForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        files = files_dict.get("files", []) if isinstance(files_dict, dict) else []

        if len(files) > 10:
            self.add_error("files", "Only 10 files allowed.")

        if files:
            self.fields["files"].queryset = files

        teammates = user.teammates.all()
        self.fields["assigned_to"].queryset = teammates
        projects = Project.objects.filter(owner=user)
        self.fields["project"].queryset = projects


class TaskCreateFromProjectForm(ModelForm):
    files = MultipleFileField(max_files=10, required=False)

    class Meta:
        model = Task
        fields = [
            "title",
            "body",
            "deadline",
            "priority",
            "assigned_to",
            "files",
        ]
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

        assignee = self.instance.project.participants.all()
        self.fields["assigned_to"].queryset = assignee
        self.fields["assigned_to"].widget.attrs["class"] = "form-control"


class CommentForm(ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control rounded-3 form-comment",
                "id": "task-chat-input",
                "placeholder": "Enter Your Message Here",
                "rows": "7",
            }
        ),
        required=False,
    )
    files = MultipleFileField(max_files=10, required=False)

    class Meta:
        model = Comment
        fields = ["body", "files"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields["body"].label = ""
        self.fields["files"].label = ""
        self.fields["files"].widget.attrs[
            "class"
        ] = "form-control comment-upload mt-3 border-0 bg-dark d-flex"
        self.fields["files"].widget.attrs["style"] = "max-width: 350px;"
        self.fields["files"].widget.attrs["value"] = "Upload"

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        files = cleaned_data.get("files")

        if not body and not files:
            raise ValidationError("Comment should contain text or attachments.")

        return cleaned_data

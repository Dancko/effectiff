from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model

from projects.models import Project


User = get_user_model()


class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(ProjectCreationForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ProjectAddParticipantsForm(ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control overflow-hidden"}),
    )

    class Meta:
        model = Project
        fields = ["participants"]

    def __init__(self, *args, **kwargs):
        super(ProjectAddParticipantsForm, self).__init__(*args, **kwargs)

        participants = self.instance.owner.teammates.all()
        self.fields["participants"].queryset = participants
        self.fields["participants"].label = ""

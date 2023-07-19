from django.forms import ModelForm

from core.models import Project


class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'category', 'description']


class ProjectAddParticipantsForm(ModelForm):
    class Meta:
        model = Project
        fields = ['participants']

    def __init__(self, *args, **kwargs):
        super(ProjectAddParticipantsForm, self).__init__(*args, **kwargs)

        participants = self.instance.owner.teammates.all()
        self.fields['participants'].queryset = participants

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    """Login form."""

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password1", "password2"]
        help_text = None

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["name", "password1", "password2"]:
            self.fields[fieldname].help_text = None


class ChangeUserForm(ModelForm):
    """Edit user info form."""

    profile_photo = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-secondary text-dark"})
    )

    class Meta:
        model = get_user_model()
        fields = [
            "name",
            "profile_photo",
            "intro",
            "bio",
            "location",
        ]

    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

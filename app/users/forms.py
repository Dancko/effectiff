from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from django.forms import ModelForm

from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    """Login form."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email"}
        ),
        label="",
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Name"}
        ),
        label="",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        ),
        label="",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Your Password"}
        ),
        label="",
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""


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


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter New Password", "class": "form-control"}
        ),
        label="",
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Your Password", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]

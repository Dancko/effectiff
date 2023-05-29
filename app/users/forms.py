from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    """Login form."""
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password1', 'password2']

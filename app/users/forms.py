from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    """Login form."""
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password1', 'password2']
        help_text = None

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

import pytest

from pytest_factoryboy import register
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from unittest.mock import MagicMock
from unittest.mock import patch


from .factories import UserFactory
from users.forms import SetPasswordForm


class MockSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_provider(self, request, provider, client_id=None, **kwargs):
        # Create a mock SocialApp instance with placeholder credentials
        mock_social_app = MagicMock(
            provider=provider, client_id="mock_client_id", secret="mock_secret"
        )
        return mock_social_app


# @pytest.fixture
# def mock_set_password_form_clean():
#     with patch("users.forms.SetPasswordForm.clean") as mock_clean:
#         yield mock_clean


@pytest.fixture
def mocked_submit():
    with patch("captcha.fields.client.submit") as mock_submit:
        yield mock_submit


register(UserFactory)

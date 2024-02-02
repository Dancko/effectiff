import pytest

from pytest_factoryboy import register
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from unittest.mock import MagicMock
from unittest.mock import patch


from .factories import UserFactory
from projects.tests.factories import ProjectFactory


class MockSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_provider(self, request, provider, client_id=None, **kwargs):
        # Create a mock SocialApp instance with placeholder credentials
        mock_social_app = MagicMock(
            provider=provider, client_id="mock_client_id", secret="mock_secret"
        )
        return mock_social_app


register(UserFactory)
register(ProjectFactory)

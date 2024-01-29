import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from .conftest import MockSocialAccountAdapter


pytestmark = pytest.mark.django_db


# ------------------------Unauthed tests-------------


def test_get_login_register_page_success(client):
    """Test get login and register page is success."""

    url = reverse("login")

    res = client.get(url)

    assert res.status_code == 200


@pytest.mark.django_db
@patch(
    "allauth.socialaccount.adapter.DefaultSocialAccountAdapter",
    MockSocialAccountAdapter,
)
def test_register_page_get_request(client):
    """Test register page get request is a success."""
    url = reverse("register")
    response = client.get(url)

    assert response.status_code == 200

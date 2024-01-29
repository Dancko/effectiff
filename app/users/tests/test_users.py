import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from .conftest import MockSocialAccountAdapter


pytestmark = pytest.mark.django_db


# ------------------------Unauthed tests-------------


@pytest.mark.parametrize(
    "test_url", ["login", "password_reset", "password_reset_sent", "verification_sent"]
)
def test_get_login_register_page_success(client, test_url):
    """Test get login and register page is success."""

    url = reverse(test_url)

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


# ---------------Authed Tests Get Requests-------------------


@pytest.mark.parametrize("test_url", ["logout", "change_password", "my_team"])
def test_get_requests_without_args(client, user_factory, test_url):
    """Test get requests of pages without args that require authentication is a success."""

    user = user_factory()
    client.force_login(user)
    url = reverse(test_url)

    res = client.get(url)

    assert res.status_code == 200


@pytest.mark.parametrize("test_url", ["profile", "add_teammate"])
def test_get_requests_with_args(client, user_factory, test_url):
    """Test get requests of pages with args that require authentication is a success."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="bobb@example.com")
    url = reverse(test_url, args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 200


def test_edit_profile_get(client, user_factory):
    """Test edit profile page get request."""

    user = user_factory()
    client.force_login(user)
    url = reverse("edit_profile", args=[user.uuid])

    res = client.get(url)

    assert res.status_code == 200


def test_delete_teammate_get(client, user_factory):
    """Test delete from team page get request."""

    user1 = user_factory()
    user2 = user_factory(email="bobb@example.com")
    user1.teammates.add(user2)
    client.force_login(user1)
    url = reverse("delete_teammate", args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 200

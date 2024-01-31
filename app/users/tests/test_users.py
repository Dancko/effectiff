import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from .conftest import MockSocialAccountAdapter


pytestmark = pytest.mark.django_db


# ------------------------Unauthed tests GET requests-------------


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


# ----------------Unauthed tests POST requests------------------
@pytest.mark.django_db
def test_login_post_success(client, user_factory):
    """Test login post is success."""

    user_factory(email="test@example.com")

    url = reverse("login")

    data = {
        "email": "test@example.com",
        "password": "test123",
    }
    res = client.post(url, data)

    assert res.status_code == 302
    assert res.url == reverse("my_tasks")


# ---------------Authed tests GET requests-------------------


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


def test_edit_profile_get_redirect(client, user_factory):
    """Test edit profile page get request redirect for not owner of page."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="test2@example.com")
    url = reverse("edit_profile", args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("my_tasks")


def test_delete_teammate_get(client, user_factory):
    """Test delete from team page get request."""

    user1 = user_factory()
    user2 = user_factory(email="bobb@example.com")
    user1.teammates.add(user2)
    client.force_login(user1)
    url = reverse("delete_teammate", args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 200


def test_register_page_redirect(client, user_factory):
    """Test register page redirect if user is authenticated."""

    user = user_factory()
    client.force_login(user)
    url = reverse("register")

    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("my_tasks")


def test_add_to_team_get_redirect(client, user_factory):
    """Test add to team redirect when the user is already a teammate."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="test1@example.com")
    user.teammates.add(user2)
    url = reverse("add_teammate", args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("profile", args=[user2.uuid])


@pytest.mark.django_db
def test_delete_from_team_get_redirect(client, user_factory):
    """Test delete from team get redirect when the user not in teammates."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="test1@example.com")
    url = reverse("delete_teammate", args=[user2.uuid])

    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("profile", args=[user2.uuid])


# -------------------Authed post requests tests-------------


def test_logout_post_success(client, user_factory):
    """Test logout page post request is a success."""

    user = user_factory()
    client.force_login(user)
    url = reverse("logout")
    data = {}

    res = client.post(url, data)
    session_user = client.session.get("_auth_user_id")

    assert res.status_code == 302
    assert res.url == reverse("register")
    assert session_user is None


def test_edit_profile_post_success(client, user_factory):
    """Test edit profile page post request is a success."""

    user = user_factory(name="Bobb")
    client.force_login(user)
    url = reverse("edit_profile", args=[user.uuid])

    data = {
        "name": "Albert",
        "profile_photo": "",
        "intro": "",
        "bio": "Hi There",
        "location": "London",
    }

    res = client.post(url, data)

    updated_user = get_user_model().objects.get(uuid=user.uuid)

    assert res.status_code == 302
    assert res.url == reverse("profile", args=[user.uuid])
    assert updated_user.name == "Albert"
    assert updated_user.location == "London"
    assert updated_user.bio == "Hi There"


def test_add_to_team_post(client, user_factory):
    """Test add to team post request is a success."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="test1@example.com")
    url = reverse("add_teammate", args=[user2.uuid])
    data = {}

    res = client.post(url, data)

    assert res.status_code == 302
    assert res.url == reverse("profile", args=[user2.uuid])
    assert user2 in user.teammates.all()


def test_delete_from_team_post(client, user_factory):
    """Test delete from team post request is a success."""

    user = user_factory()
    client.force_login(user)
    user2 = user_factory(email="test1@example.com")
    user.teammates.add(user2)
    url = reverse("delete_teammate", args=[user2.uuid])
    data = {}

    res = client.post(url, data)

    assert res.status_code == 302
    assert res.url == reverse("profile", args=[user2.uuid])
    assert len(user.teammates.filter(id=user2.id)) == 0

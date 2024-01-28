import pytest

from django.contrib.auth import get_user_model, login, authenticate
from django.urls import reverse

from projects.models import Project


pytestmark = pytest.mark.django_db


# ----------Tests with unauthed users----------------------


@pytest.mark.parametrize(
    "test_url", ["project", "edit_project", "delete_project", "add_members"]
)
def test_projects_views_unauth_redirect_with_args(client, project_factory, test_url):
    """Test unauthed user is redirected to login page from project urls with args."""

    project = project_factory()

    url = reverse(test_url, args=[project.uuid])

    res = client.get(url)

    assert res.status_code == 302
    assert reverse("login") in res.url


@pytest.mark.parametrize("test_url", ["my_projects", "create_project"])
def test_projects_views_unauth_redirect_without_args(client, project_factory, test_url):
    """Test unauthed user is redirected to login page from project urls without args."""

    url = reverse(test_url)
    res = client.get(url)

    assert res.status_code == 302
    assert reverse("login") in res.url


# ---------------Authed tests---------------------


def test_myprojects_get_success(client, project_factory):
    """Test get request for my projects is a success."""

    project = project_factory(title="Test")
    user = project.owner
    client.force_login(user)

    url = reverse("my_projects")

    res = client.get(url)

    assert res.status_code == 200


def test_project_detail_get_success(client, project_factory):
    """Test get request for project detail is a success."""

    project = project_factory(title="Test")
    user = project.owner

    client.force_login(user)
    url = reverse("my_projects")
    res = client.get(url)

    res.status_code == 200

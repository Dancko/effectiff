import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse


pytestmark = pytest.mark.django_db

User = get_user_model()


def test_redirect_unauthed_home_page(client):
    """Test homepage status code 302 for unauthed users."""

    url = reverse("my_tasks")
    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("login") + "?next=/"


@pytest.mark.parametrize(
    "test_url",
    ["task_detail", "edit_task", "delete_task", "change_assignee", "change_st"],
)
def test_redirect_logout_user(client, create_test_task, test_url):
    """Test redirect a logged out user from pages that require auth."""
    test_task = create_test_task

    url = reverse(test_url, args=[test_task.uuid])
    res = client.get(url)

    assert res.status_code == 302


@pytest.mark.parametrize("test_url", ["my_tasks", "create_task"])
def test_get_homepage_auth(client, create_testuser, test_url):
    """Test homepage and create_task status code 200 for authed users."""

    create_testuser
    url = reverse(test_url)

    client.login(email="test@example.com", password="pass123")
    res = client.get(url)

    assert res.status_code == 200


def test_task_get(client):
    pass

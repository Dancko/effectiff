import pytest
import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from tasks.models import Comment, CommentFile, Task


pytestmark = pytest.mark.django_db

User = get_user_model()


# ---------------------Unauthed tests-------------------


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
def test_redirect_logout_user(client, task_factory, test_url):
    """Test redirect a logged out user from pages that require auth."""
    test_task = task_factory()

    url = reverse(test_url, args=[test_task.uuid])
    res = client.get(url)

    assert res.status_code == 302


# -------------------------Authed Tests----------------------


@pytest.mark.parametrize("test_url", ["my_tasks", "create_task"])
def test_get_homepage_auth(client, user_factory, test_url):
    """Test homepage and create_task status code 200 for authed users."""

    user = user_factory(email="testuser@example.com", password="test123", name="Test")
    url = reverse(test_url)
    client.force_login(user)

    res = client.get(url)

    assert res.status_code == 200


def test_task_detail_get(client, task_factory):
    """Test task detail page get request."""
    task = task_factory()
    user = task.project.owner
    url = reverse("task_detail", args=[task.uuid])
    client.force_login(user)

    res = client.get(url)

    assert res.status_code == 200


def test_task_detail_comment_post(client, task_factory):
    """Test leaving comments post request."""
    task = task_factory()
    user = task.project.owner
    url = reverse("task_detail", args=[task.uuid])
    client.force_login(user)

    file_content = b"Test"
    file = SimpleUploadedFile("test_file.txt", file_content)

    data = {"body": "test message", "files": file}

    res = client.post(url, data)

    assert res.status_code == 302
    assert res.url == reverse("task_detail", args=[task.uuid])
    assert Comment.objects.filter(body="test message")
    assert CommentFile.objects.filter(file__icontains="test_file")


def test_change_status_get(client, task_factory):
    """Test change status get request."""

    task = task_factory()
    url = reverse("change_st", args=[task.uuid])
    user = task.project.owner
    client.force_login(user)

    res = client.get(url)

    assert res.status_code == 200


def test_change_status_post(client, task_factory):
    """Test change status post request."""

    task = task_factory()
    url = reverse("change_st", args=[task.uuid])
    user = task.project.owner
    client.force_login(user)

    data = {"status": "In Progress"}

    res = client.post(url, data)

    updated_task = Task.objects.get(id=task.id)

    assert res.status_code == 302
    assert res.url == reverse("task_detail", args=[task.uuid])
    assert updated_task.status == "In Progress"


def test_task_create_post(client, project_factory, user_factory):
    """Test creating tasks is success."""

    project = project_factory()
    user = project.owner
    user2 = user_factory(email="test1@example.com")

    user.teammates.add(user2)
    user2 = user.teammates.first()
    client.force_login(user)
    url = reverse("create_task")

    file_content = b"Test"
    file = SimpleUploadedFile("test.txt", file_content)

    data = {
        "project": project.id,
        "title": "Test Form Task",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
        "files": file,
    }

    res = client.post(url, data)

    assert res.status_code == 302
    assert res.url == reverse("my_tasks")

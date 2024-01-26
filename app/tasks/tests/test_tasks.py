import pytest
import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.urls import reverse

from tasks.models import Comment, CommentFile, Task, TaskFile


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


@pytest.mark.parametrize(
    "test_url",
    ["task_detail", "edit_task", "delete_task", "change_assignee", "change_st"],
)
def test_get_login_user_success(client, task_factory, test_url):
    """Test get request 200 for logged in users."""
    test_task = task_factory()
    user = test_task.project.owner
    client.force_login(user)

    url = reverse(test_url, args=[test_task.uuid])
    res = client.get(url)

    assert res.status_code == 200


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
    default_storage.delete(file.name)

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
    default_storage.delete(file.name)

    assert res.status_code == 302
    assert res.url == reverse("my_tasks")


def test_task_create_from_project_post(client, project_factory, user_factory):
    """Test creating tasks from project is success."""

    project = project_factory()
    user = project.owner
    user2 = user_factory(email="test1@example.com")
    project.participants.add(user2)

    user.teammates.add(user2)
    user2 = user.teammates.first()
    client.force_login(user)
    url = reverse("create_task_from_project", args=[project.uuid])

    file_content = b"Test"
    file = SimpleUploadedFile("test.txt", file_content)

    data = {
        "title": "Test Form Task",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
        "files": [file],
    }

    res = client.post(url, data)
    default_storage.delete(file.name)

    assert res.status_code == 302
    assert res.url == reverse("my_projects")


def test_create_task_from_project_get(client, project_factory):
    """Test create task from project page get request."""
    project = project_factory()
    user = project.owner
    client.force_login(user)
    url = reverse("create_task_from_project", args=[project.uuid])

    res = client.get(url)

    assert res.status_code == 200


def test_task_edit_page_post_deleting_files(client, task_factory):
    """Test task edit page post request when no new files provided."""

    task = task_factory(title="Test Task")
    user = task.project.owner
    user2 = task.assigned_to
    user.teammates.add(user2)
    client.force_login(user)
    url = reverse("edit_task", args=[task.uuid])

    file_content = b"Test"
    file = SimpleUploadedFile("test.txt", file_content)

    TaskFile.objects.create(task=task, file=file)

    data = {
        "project": task.project.id,
        "title": "Test Form Task (Edited)",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
        "files": "",
    }

    res = client.post(url, data)

    edited_task = Task.objects.get(id=task.id)

    assert res.status_code == 302
    assert res.url == reverse("task_detail", args=[task.uuid])
    assert edited_task.title == "Test Form Task (Edited)"
    assert len(edited_task.files.all()) == 0


def test_task_edit_page_post_new_file(client, task_factory):
    """Test task edit page post request with file."""

    task = task_factory(title="Test Task")
    user = task.project.owner
    user2 = task.assigned_to
    user.teammates.add(user2)
    client.force_login(user)
    url = reverse("edit_task", args=[task.uuid])

    file_content = b"Test FIle for editing a task"
    file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

    data = {
        "project": task.project.id,
        "title": "Test Form Task (Edited)",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
        "files": file,
    }

    res = client.post(url, data=data)

    edited_task = Task.objects.get(id=task.id)

    assert res.status_code == 302
    assert res.url == reverse("task_detail", args=[task.uuid])
    assert edited_task.title == "Test Form Task (Edited)"
    assert len(edited_task.files.all()) == 1

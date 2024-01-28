import pytest

from django.contrib.auth import get_user_model, login, authenticate
from django.urls import reverse

from projects.models import Project, ProjectFile
from .conftest import create_projectfile, delete_projectfile


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


@pytest.mark.parametrize(
    "test_url", ["project", "edit_project", "delete_project", "add_members"]
)
def test_project_pages_with_args_get(client, project_factory, test_url):
    """Test get request for views with args in urls."""

    project = project_factory(title="Test")
    user = project.owner
    client.force_login(user)
    url = reverse(test_url, args=[project.uuid])

    res = client.get(url)

    assert res.status_code == 200


@pytest.mark.parametrize("test_url", ["my_projects", "create_project"])
def test_project_pages_no_args_get(client, user_factory, test_url):
    """Test get project pages with no args is success."""

    user = user_factory()
    client.force_login(user)

    url = reverse(test_url)

    res = client.get(url)

    assert res.status_code == 200


def test_create_project_with_multiple_files_post(client, user_factory):
    """Test post request for creating new project page with multiple files."""

    user = user_factory(name="Test User")
    client.force_login(user)
    url = reverse("create_project")

    file1 = create_projectfile(filename="test_file_1.txt")
    file2 = create_projectfile(filename="test_file_2.pdf")

    data = {
        "title": "Test Project Create",
        "description": "test description of creating a file",
        "files": [file1, file2],
    }

    res = client.post(url, data)
    project = Project.objects.get(title="Test Project Create")

    delete_projectfile(file1)
    delete_projectfile(file2)

    assert res.status_code == 302
    assert res.url == reverse("my_projects")
    assert project is not None
    assert len(project.project_files.all()) == 2


def test_edit_project_with_files_post(client, project_factory):
    """Test updating existing project info is success."""
    project = project_factory(title="Test project")
    user = project.owner
    client.force_login(user)
    url = reverse("edit_project", args=[project.uuid])

    file1 = create_projectfile(filename="test1.pdf")
    file2 = create_projectfile(filename="test2.pdf")

    data = {
        "title": "Test Project (Edited)",
        "description": "test description of updating a project",
        "files": [file1, file2],
    }

    res = client.post(url, data)

    edited_project = Project.objects.get(id=project.id)

    delete_projectfile(file1)
    delete_projectfile(file2)

    assert res.status_code == 302
    assert res.url == reverse("project", args=[project.uuid])
    assert edited_project.title == "Test Project (Edited)"
    assert edited_project.description == "test description of updating a project"
    assert len(edited_project.project_files.all()) == 2

import pytest

from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import reverse

from core.models import Project


pytestmark = pytest.mark.django_db


def test_myprojects_get_success(request, client):
    """Test get request for authed user is a success."""
    user = get_user_model().objects.create_user(
        email="test@example.com", password="testpass123"
    )
    project = Project.objects.create(name="TestProj", owner=user)
    project.participants.add(user)
    client.login(email=user.email, password="testpass123")
    url = reverse("my_projects", args=[str(user.uuid)])

    res = client.get(url)

    assert res.status_code == 200
    assert project.name in str(res.content)
    assert project.owner == user
    assert user in project.participants.all()


def test_my_project_unauth_redirect(client):
    """Test unauthed user is redirected to login page."""
    user = get_user_model().objects.create_user(
        email="test@example.com", password="testpass123"
    )
    project = Project.objects.create(name="TestProj", owner=user)
    url = reverse("my_projects", args=[str(user.uuid)])

    res = client.get(url)

    assert res.status_code == 302

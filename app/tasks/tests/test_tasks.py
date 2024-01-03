import pytest

from django.contrib.auth import get_user_model, login, authenticate
from django.urls import reverse

from users import views


pytestmark = pytest.mark.django_db

User = get_user_model()


def test_redirect_unathed_home_page(client):
    """Test homepage status code 302 for unauthed users."""
    url = reverse("my_tasks")
    res = client.get(url)

    assert res.status_code == 302
    assert res.url == reverse("login") + "?next=/"


def test_get_homepage_authed(client):
    """Test homepage status code 200 for authed users."""
    user = User.objects.create_user(email="test@example.com", password="test123")
    url = reverse("my_tasks")

    client.login(email="test@example.com", password="test123")
    res = client.get(url)

    assert res.status_code == 200

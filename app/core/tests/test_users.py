import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse


pytestmark = pytest.mark.django_db

def test_creating_new_user():
    """Test creating new users."""
    user = get_user_model().objects.create_user(email='test@example.com', password='test123', name='Test')

    assert user.email == 'test@example.com'
    assert user.name == 'Test'
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False


def test_create_superuser():
    """Test creating superuser."""
    user = get_user_model().objects.create_superuser(email='test_super@example.com', password='test123', name='super')

    assert user.email == 'test_super@example.com'
    assert user.name == 'super'
    assert user.is_active == True
    assert user.is_staff == True
    assert user.is_superuser == True


def test_get_home_page(client):
    """Test homepage status code 200."""
    url = reverse('home')
    res = client.get(url)

    assert res.status_code == 200


def test_get_login_page_success(client):
    """Test getting login page returns 200 status code."""
    url = reverse('login')
    res = client.get(url)

    assert res.status_code == 200


def test_get_register_page(client):
    """Test getting register page returns 200 status code."""
    url = reverse('register')
    res = client.get(url)

    assert res.status_code == 200

import pytest

from core.models import User


pytestmark = pytest.mark.django_db

def test_creating_new_user():
    """Test creating new users."""
    user = User.objects.create_user(email='test@example.com', password='test123', name='Test')

    assert user.email == 'test@example.com'
    assert user.name == 'Test'
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False


def test_create_superuser():
    """Test creating superuser."""
    user = User.objects.create_superuser(email='test_super@example.com', password='test123', name='super')

    assert user.email == 'test_super@example.com'
    assert user.name == 'super'
    assert user.is_active == True
    assert user.is_staff == True
    assert user.is_superuser == True

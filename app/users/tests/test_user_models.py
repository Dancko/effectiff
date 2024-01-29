import pytest

from django.contrib.auth import get_user_model

from users.models import Skill


def test_create_user_method_with_no_email_fails():
    """Test create_user method of User Manager without providing an error will raise ValueError."""

    with pytest.raises(ValueError, match="A user must have an email."):
        # Call the method without providing an email
        get_user_model().objects.create_user(email="")


@pytest.mark.django_db
def test_create_superuser():
    """Test creating superuser with UserManager."""

    user = get_user_model().objects.create_superuser(
        email="super@example.com", password="test123"
    )

    assert user.is_superuser == True
    assert user.is_staff == True


@pytest.mark.django_db
def test_user_return_str(user_factory):
    """Test user __str__ must return user.name."""

    user = user_factory(name="John")

    assert user.__str__() == "John"


@pytest.mark.django_db
def test_skill_return_str():
    """Test skill __str__ must return skill.name."""

    skill = Skill.objects.create(name="Django")

    assert skill.__str__() == "Django"

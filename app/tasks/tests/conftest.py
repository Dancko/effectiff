import pytest

from users.models import User

# from django.contrib.auth import get_user_model

# User = get_user_model()


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "testuser", "password": "pass123"}


@pytest.fixture
def create_testuser(user_data):
    test_user = User.objects.create_user(**user_data)
    return test_user

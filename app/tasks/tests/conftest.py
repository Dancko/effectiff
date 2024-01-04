import pytest
import datetime

from users.models import User
from projects.models import Project
from tasks.models import Task

# from django.contrib.auth import get_user_model

# User = get_user_model()


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "testuser", "password": "pass123"}


@pytest.fixture
def create_testuser(user_data):
    """Fixture for creating a user in tests."""

    test_user = User.objects.create_user(**user_data)
    return test_user


@pytest.fixture
def create_test_task(create_testuser, user_data):
    """Fixture for creating a test task."""

    test_user = create_testuser
    test_project = Project.objects.create(title="Test Project", owner=test_user)
    test_task = Task.objects.create(
        title="Test Task",
        project=test_project,
        deadline=datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        assigned_to=test_user,
    )

    return test_task

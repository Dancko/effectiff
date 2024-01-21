import pytest
import datetime

from pytest_factoryboy import register

from django.core.files.storage import default_storage

from users.models import User
from projects.models import Project
from tasks.models import Task, TaskFile

from .factories import TaskFactory, CommentFactory
from users.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory

# from django.contrib.auth import get_user_model

# User = get_user_model()

register(TaskFactory)
register(CommentFactory)
register(UserFactory)
register(ProjectFactory)


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "testuser", "password": "pass123"}


@pytest.fixture
def create_testuser(user_data):
    """Fixture for creating a user in tests."""

    test_user = User.objects.create_user(**user_data)
    return test_user


@pytest.fixture
def create_test_project(create_testuser):
    """Fixture for creating a test project."""

    test_user = create_testuser
    test_project = Project.objects.create(title="Test Project", owner=test_user)
    return test_project


@pytest.fixture
def create_test_task(create_test_project, create_testuser):
    """Fixture for creating a test task."""

    test_user = create_testuser
    test_project = create_test_project

    test_task = Task.objects.create(
        title="Test Task",
        project=test_project,
        deadline=datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        assigned_to=test_user,
    )

    return test_task


@pytest.fixture
def cleanup_files(request):
    created_files = []

    def cleanup():
        for file in created_files:
            default_storage.delete(file["path"])

        TaskFile.objects.filter(id__in=[file["id"] for file in created_files]).delete()

    request.addfinalizer(cleanup)

    return created_files

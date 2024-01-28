import pytest

from pytest_factoryboy import register

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

from .factories import ProjectFactory
from users.tests.factories import UserFactory
from tasks.tests.factories import TaskFactory


register(ProjectFactory)
register(UserFactory)
register(TaskFactory)


def delete_projectfile(file_name):
    """Fixture for deleting project files after tests."""
    default_storage.delete(f"project_attachments/{file_name}")


def create_projectfile(filename="testfile.txt"):
    """Function for creating a projectfile."""

    file_content = b"test"
    return SimpleUploadedFile(filename, file_content)

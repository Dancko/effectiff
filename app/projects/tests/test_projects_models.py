import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from projects.models import Project, ProjectFile, Category
from .conftest import delete_projectfile, create_projectfile


pytestmark = pytest.mark.django_db


def test_project_return_str(project_factory):
    """Test str method of project object returns title."""
    project = project_factory(title="Test Project")

    assert Project.objects.get(id=project.id).__str__() == "Test Project"


def test_project_file_return_str(project_factory):
    """Test projectfile str method return short_name."""
    project = project_factory()

    file_content = b"Test File"
    file_name = "test_project_file_return_str.txt"

    file = SimpleUploadedFile(file_name, file_content)

    project_file = ProjectFile.objects.create(project=project, file=file)

    delete_projectfile(file_name)

    assert project_file.__str__() == "test_project_file_return_str.txt"[-20:]


def test_project_file_get_ext(project_factory):
    """Test projectfile get_ext method returns extension of a file."""
    project = project_factory()
    file = create_projectfile(filename="test_project_file_get_ext.txt")
    projectfile = ProjectFile.objects.create(project=project, file=file)

    delete_projectfile("test_project_file_get_ext.txt")

    assert projectfile.get_ext == "txt"


def test_category_return_str():
    """Test category str method returns title."""

    category = Category.objects.create(title="Test")

    assert category.__str__() == "Test"

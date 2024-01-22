import pytest
import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from tasks import forms


@pytest.mark.django_db
def test_TaskCreateForm(user_factory, project_factory):
    """Test form for creating tasks."""

    user1 = user_factory(email="test@example.com")

    user2 = user_factory(email="test1@example.com")

    user1.teammates.add(user2)

    test_project = project_factory(owner=user1)

    data = {
        "project": test_project.id,
        "title": "Test Form Task",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
        "files": "",
    }

    form = forms.TaskCreateForm(
        user=user1,
        data=data,
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_taskCreateForm_too_many_files(user_factory, project_factory):
    """Test attempt to upload more than 10 files will raise error."""
    user1 = user_factory(email="test@example.com")

    user2 = user_factory(email="test1@example.com")

    user1.teammates.add(user2)

    test_project = project_factory(owner=user1)

    file_content = b"Test FIle"
    files = [SimpleUploadedFile(f"test_file_{i}.txt", file_content) for i in range(15)]
    files = {"files": files}

    data = {
        "project": test_project.id,
        "title": "Test Form Task",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
    }

    form = forms.TaskCreateForm(user=user1, data=data, files=files)

    assert form.is_valid() == False


@pytest.mark.django_db
def test_TaskCreateFromProjectForm(project_factory, user_factory):
    """Test form for creating tasks thru projects."""

    project = project_factory(
        participants=[
            user_factory(),
        ]
    )

    user2 = project.participants.first()

    form = forms.TaskCreateFromProjectForm(
        project=project,
        data={
            "title": "Test Form Task",
            "body": "",
            "deadline": datetime.datetime(
                2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc
            ),
            "priority": "Moderate",
            "assigned_to": user2.id,
        },
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_TaskAddPartiicipantsForm(task_factory, project_factory, user_factory):
    """Test form for adding participants to tasks."""

    task = task_factory(project=project_factory(participants=[user_factory()]))
    user2 = task.project.participants.first()

    form = forms.TaskAddPartiicipantsForm(instance=task, data={"assigned_to": user2})

    assert form.is_valid()


def test_CommentForm():
    """Test form for adding comments."""

    form = forms.CommentForm(data={"body": "test message"})

    assert form.is_valid()


@pytest.mark.django_db
def test_TaskCreateForm_uploading_files(user_factory, project_factory):
    """Test uploading file into task creation form."""

    file_content = b"Test File Content"
    test_file = SimpleUploadedFile("test_file.txt", file_content)
    test_file2 = SimpleUploadedFile("test_file2.pdf", file_content)

    user1 = user_factory(email="test@example.com")

    user2 = user_factory(email="test1@example.com")

    user1.teammates.add(user2)

    test_project = project_factory(owner=user1)

    data = {
        "project": test_project.id,
        "title": "Test Form Task",
        "body": "",
        "deadline": datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc),
        "priority": "Moderate",
        "assigned_to": user2.id,
    }

    files = {"files": [test_file, test_file2]}

    form = forms.TaskCreateForm(user=user1, data=data, files=files)

    assert form.is_valid()


@pytest.mark.django_db
def test_TaskCreateFromProjectForm_uploading_files(project_factory, user_factory):
    """Test form for creating tasks thru projects with multiple files upload."""

    project = project_factory(
        participants=[
            user_factory(),
        ]
    )

    user2 = project.participants.first()

    file_content = b"Test File Content"
    file1 = SimpleUploadedFile("file.pdf", file_content)
    file2 = SimpleUploadedFile("file2.txt", file_content)
    files = {
        "files": [file1, file2],
    }

    form = forms.TaskCreateFromProjectForm(
        project=project,
        data={
            "title": "Test Form Task",
            "body": "",
            "deadline": datetime.datetime(
                2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc
            ),
            "priority": "Moderate",
            "assigned_to": user2.id,
        },
        files=files,
    )

    assert form.is_valid()


def test_CommentForm_uploading_files():
    """Test form for adding comments with attachments."""

    file_content = b"Test File Content"
    file1 = SimpleUploadedFile("file1.txt", file_content)
    file2 = SimpleUploadedFile("file2.pdf", file_content)

    data = {"body": "test message"}
    files = {"files": [file1, file2]}

    form = forms.CommentForm(data=data, files=files)

    assert form.is_valid()


def test_CommentForm_uploading_files_no_body():
    """Test form for adding no-text-comments with attachments."""

    file_content = b"Test File Content"
    file1 = SimpleUploadedFile("file1.txt", file_content)
    file2 = SimpleUploadedFile("file2.pdf", file_content)

    files = {"files": [file1, file2]}

    data = {"body": ""}

    form = forms.CommentForm(data=data, files=files)

    assert form.is_valid()


def test_CommentForm_totally_blank():
    """Test form for adding comments with neither test nor files should be invalid."""

    data = {"body": ""}
    files = {"files": ""}

    form = forms.CommentForm(data=data, files=files)

    assert form.is_valid() == False

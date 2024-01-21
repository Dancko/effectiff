import pytest
import datetime
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from tasks.models import TaskFile


pytestmark = pytest.mark.django_db


def test_task_str_return(task_factory):
    task = task_factory(title="Test Task 1")

    assert task.__str__() == "Test Task 1"


def test_task_isoutdated_false(task_factory):
    task = task_factory(title="Test task 1")

    assert task.is_outdated() == False


def test_task_isoutdated_true(task_factory):
    task = task_factory(
        deadline=datetime.datetime(2023, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
    )

    assert task.is_outdated() == True


def test_comment_str_return(comment_factory):
    comment = comment_factory(body="Hello")

    assert comment.__str__() == "Hello"


def test_task_file_str_return(task_factory, cleanup_files):
    task = task_factory(title="Test Task With File")
    timestamp = int(time.time())

    file_content = b"Test File"
    filename = f"testfile1_{timestamp}"
    file = SimpleUploadedFile(filename, file_content)

    task_file = TaskFile.objects.create(task=task, file=file)

    cleanup_files.append({"path": task_file.file.path, "id": task_file.id})
    assert task_file.__str__() == filename


def test_task_file_get_ext(task_factory, cleanup_files):
    task = task_factory(title="Test task with files")
    file_content = b"Test File"
    filename = f"testfile1.txt"
    file = SimpleUploadedFile(filename, file_content)
    task_file = TaskFile.objects.create(task=task, file=file)
    cleanup_files.append({"path": task_file.file.path, "id": task_file.id})

    assert task_file.get_ext == "txt"

import pytest
import datetime


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

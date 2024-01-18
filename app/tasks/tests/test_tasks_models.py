import pytest


@pytest.mark.django_db
def test_task_str_return(task_factory):
    task = task_factory(title="Test Task 1")

    assert str(task) == "Test Task 1"

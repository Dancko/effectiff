import pytest
import datetime

from django.contrib.auth import get_user_model

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
            "files": "",
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


@pytest.mark.django_db
def test_CommentForm(create_test_task):
    """Test form for adding comments."""

    form = forms.CommentForm(data={"body": "test message"})

    assert form.is_valid()

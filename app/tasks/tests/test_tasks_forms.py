import pytest
import datetime

from django.contrib.auth import get_user_model

from tasks import forms


@pytest.mark.django_db
def test_TaskCreateForm(create_testuser, create_test_project):
    """Test form for creating tasks."""

    user1 = create_testuser
    user2 = get_user_model().objects.create_user(
        email="tom@example.com", password="test123"
    )

    user1.teammates.add(user2)
    test_project = create_test_project

    form = forms.TaskCreateForm(
        user=user1,
        data={
            "project": test_project.id,
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
def test_TaskCreateFromProjectForm(create_test_project):
    """Test form for creating tasks thru projects."""

    project = create_test_project
    user1 = project.owner
    user2 = get_user_model().objects.create_user(
        email="tom@example.com", password="test123"
    )
    user1.teammates.add(user2)
    project.participants.add(user2)

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
def test_TaskAddPartiicipantsForm(create_test_task):
    """Test form for adding participants to tasks."""

    task = create_test_task
    project = task.project
    user2 = get_user_model().objects.create_user(
        email="tom@example.com", password="test123"
    )
    project.participants.add(user2)

    form = forms.TaskAddPartiicipantsForm(instance=task, data={"assigned_to": user2})

    assert form.is_valid()


@pytest.mark.django_db
def test_CommentForm(create_test_task):
    """Test form for adding comments."""

    form = forms.CommentForm(data={"body": "test message"})

    assert form.is_valid()

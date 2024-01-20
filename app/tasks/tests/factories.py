import factory
import datetime

from django.contrib.auth import get_user_model

from tasks.models import Task, Comment

from users.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = "Test Task"
    deadline = datetime.datetime(2026, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
    project = factory.SubFactory(ProjectFactory)
    assigned_to = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    task = factory.SubFactory(TaskFactory)
    body = "x"

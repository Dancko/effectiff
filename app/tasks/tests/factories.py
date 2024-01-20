import factory
import datetime

from django.contrib.auth import get_user_model

from tasks.models import Task, Comment
from projects.models import Project


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"test{n}@example.com")
    password = "test123"
    name = "testuseristo"
    is_superuser = False
    is_staff = False
    is_active = True


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = "Test Project"
    owner = factory.SubFactory(UserFactory)


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

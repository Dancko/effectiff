import factory

from projects.models import Project
from users.tests.factories import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = "Test Project"
    owner = factory.SubFactory(UserFactory)

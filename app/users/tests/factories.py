import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"test{n}@example.com")
    password = "test123"
    name = "testuseristo"
    is_superuser = False
    is_staff = False
    is_active = True

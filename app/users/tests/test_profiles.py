import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Skill


pytestmark = pytest.mark.django_db

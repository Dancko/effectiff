from django.contrib.auth import get_user_model

from core.models import Project


user = get_user_model().objects.create_user(email='test@example.com', password='testpass123')

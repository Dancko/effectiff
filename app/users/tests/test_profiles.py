import sys
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_get_profile_page_success(client):
    """Test accessing a profile page is successful."""
    user = get_user_model().objects.create_user(email='testuser@example.com', password='testpass123')
    url = reverse('profile', args=[str(user.id)])

    res = client.get(url)

    sys.stdout.write(str(res.content))
    assert res.status_code == 200
    assert user.email in str(res.content)
    assert user.password not in str(res.content)

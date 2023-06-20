import pytest
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from core.models import Skill


pytestmark = pytest.mark.django_db


def test_get_profile_page_success(client):
    """Test accessing a profile page is successful."""
    user = get_user_model().objects.create_user(email='testuser@example.com', password='testpass123',
                                                location='New York', bio='Hi there!')
    django = Skill(name='Django')
    django.save()
    user.skills.add(django)
    url = reverse('profile', args=[str(user.id)])

    res = client.get(url)

    assert res.status_code == 200
    assert user.email in str(res.content)
    assert user.password not in str(res.content)
    assert user.location in str(res.content)
    assert user.bio in str(res.content)
    assert user.skills.all()[0].name in str(res.content)


def test_get_edit_profile_page_authed_success(request, client):
    """Test edit profile get request for an authorized user is success."""
    user = get_user_model().objects.create_user(email='testuser@example.com', password='testpass123', name='john')
    url = reverse('edit_profile', args=[str(user.id)])
    client.login(email=user.email, password='testpass123')

    res = client.get(url)

    assert res.status_code == 200

def test_get_edit_profile_page_unauthed_fails(client):
    """Test edit profile get request for an unauthed user fails."""
    url = reverse('edit_profile', args=[str(1)])

    res = client.get(url)

    assert res.status_code == 302

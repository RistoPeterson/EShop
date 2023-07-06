import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_example():
    user = User.objects.create_user('JoosepV', is_superuser=True)

    assert user.is_superuser == True
    assert user.username == 'JoosepV'

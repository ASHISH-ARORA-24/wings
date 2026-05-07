import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def family_user(db):
    from model_bakery import baker
    extra = baker.make('accounts.UserExtraInfo', role='family')
    return extra.user


@pytest.fixture
def vendor_user(db):
    from model_bakery import baker
    extra = baker.make('accounts.UserExtraInfo', role='vendor')
    return extra.user

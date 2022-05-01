import pytest

from . import factories


pytestmark = pytest.mark.django_db


def test_profile():
    profile = factories.ProfileFactory(
        user=factories.UserFactory(username='test')
    )
    assert str(profile) == 'test'

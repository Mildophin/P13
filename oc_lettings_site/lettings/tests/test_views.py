import pytest

from . import factories
from .. import views


pytestmark = pytest.mark.django_db


def test_index_view(rf):
    factories.LettingFactory(title='My House 1')
    factories.LettingFactory(title='My House 2')
    factories.LettingFactory(title='My House 3')

    response = views.index(rf)

    assert response.status_code == 200
    assert b'My House 1' in response.content
    assert b'My House 2' in response.content
    assert b'My House 3' in response.content


def test_profile_view(rf):
    address1 = factories.AddressFactory(
        number=100,
        street='test street',
    )
    factories.LettingFactory(title='title test', address=address1)
    response = views.letting(rf, 1)

    assert response.status_code == 200
    assert b'100' in response.content
    assert b'title test' in response.content
    assert b'test street' in response.content

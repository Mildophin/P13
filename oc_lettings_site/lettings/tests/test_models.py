import pytest

from . import factories


pytestmark = pytest.mark.django_db


def test_address():
    address = factories.AddressFactory(number=10, street='test')
    assert str(address) == '10 test'


def test_letting():
    letting = factories.LettingFactory(title='test')
    assert str(letting) == 'test'

from django.urls import resolve, reverse


def test_index():
    assert reverse('lettings:index') == '/lettings/'
    assert resolve('/lettings/').view_name == 'lettings:index'


def test_lettings():
    assert reverse('lettings:letting', kwargs={'letting_id': 1}) == '/lettings/1/'
    assert resolve('/lettings/1/').view_name == 'lettings:letting'

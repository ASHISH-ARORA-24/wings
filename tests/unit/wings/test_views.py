import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHomeView:

    def test_home_returns_200(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_uses_correct_template(self, client):
        response = client.get(reverse('home'))
        assert 'home.html' in [t.name for t in response.templates]

    def test_home_contains_site_name(self, client, settings):
        settings.SITE_NAME = 'Wing Man'
        response = client.get(reverse('home'))
        assert b'Wing Man' in response.content

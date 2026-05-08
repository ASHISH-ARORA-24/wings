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

    def test_home_accessible_without_login(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestGoogleLoginWithRoleView:

    def test_family_role_stored_in_session(self, client):
        client.get(reverse('google_login_with_role', kwargs={'role': 'family'}))
        assert client.session.get('login_role') == 'family'

    def test_vendor_role_stored_in_session(self, client):
        client.get(reverse('google_login_with_role', kwargs={'role': 'vendor'}))
        assert client.session.get('login_role') == 'vendor'

    def test_invalid_role_not_stored_in_session(self, client):
        client.get(reverse('google_login_with_role', kwargs={'role': 'admin'}))
        assert client.session.get('login_role') is None

    def test_redirects_to_google_login(self, client):
        response = client.get(reverse('google_login_with_role', kwargs={'role': 'family'}))
        assert response.status_code == 302
        assert response['Location'] == '/accounts/google/login/'

    def test_family_role_overwrites_previous_session_role(self, client):
        client.get(reverse('google_login_with_role', kwargs={'role': 'vendor'}))
        client.get(reverse('google_login_with_role', kwargs={'role': 'family'}))
        assert client.session.get('login_role') == 'family'

    def test_vendor_role_overwrites_previous_session_role(self, client):
        client.get(reverse('google_login_with_role', kwargs={'role': 'family'}))
        client.get(reverse('google_login_with_role', kwargs={'role': 'vendor'}))
        assert client.session.get('login_role') == 'vendor'

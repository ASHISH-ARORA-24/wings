import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestFamilyDashboard:

    def test_dashboard_redirects_unauthenticated_user(self, client):
        response = client.get(reverse('family:dashboard'))
        assert response.status_code == 302

    def test_unauthenticated_redirect_goes_to_login(self, client):
        response = client.get(reverse('family:dashboard'))
        assert '/accounts/login/' in response['Location']

    def test_dashboard_returns_200_for_authenticated_user(self, client, user):
        client.force_login(user)
        response = client.get(reverse('family:dashboard'))
        assert response.status_code == 200

    def test_dashboard_uses_correct_template(self, client, user):
        client.force_login(user)
        response = client.get(reverse('family:dashboard'))
        assert 'family/dashboard.html' in [t.name for t in response.templates]

    def test_dashboard_contains_site_name(self, client, user, settings):
        settings.SITE_NAME = 'Wing Man'
        client.force_login(user)
        response = client.get(reverse('family:dashboard'))
        assert b'Wing Man' in response.content

    def test_dashboard_contains_family_role_badge(self, client, user):
        client.force_login(user)
        response = client.get(reverse('family:dashboard'))
        assert b'Family' in response.content

    def test_dashboard_contains_username(self, client, user):
        client.force_login(user)
        response = client.get(reverse('family:dashboard'))
        assert user.username.encode() in response.content

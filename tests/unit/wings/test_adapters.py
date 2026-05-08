import pytest
from django.test import RequestFactory
from django.contrib.sessions.backends.db import SessionStore

from wings.adapters import RoleAwareAccountAdapter


@pytest.mark.django_db
class TestRoleAwareAccountAdapter:

    def _make_request(self, role=None):
        factory = RequestFactory()
        request = factory.get('/')
        request.session = SessionStore()
        if role:
            request.session['login_role'] = role
        return request

    def test_family_role_redirects_to_family_dashboard(self):
        request = self._make_request(role='family')
        url = RoleAwareAccountAdapter(request).get_login_redirect_url(request)
        assert url == '/family/dashboard/'

    def test_vendor_role_redirects_to_vendor_dashboard(self):
        request = self._make_request(role='vendor')
        url = RoleAwareAccountAdapter(request).get_login_redirect_url(request)
        assert url == '/vendor/dashboard/'

    def test_no_role_in_session_defaults_to_family_dashboard(self):
        request = self._make_request()
        url = RoleAwareAccountAdapter(request).get_login_redirect_url(request)
        assert url == '/family/dashboard/'

    def test_invalid_role_defaults_to_family_dashboard(self):
        request = self._make_request(role='superadmin')
        url = RoleAwareAccountAdapter(request).get_login_redirect_url(request)
        assert url == '/family/dashboard/'

    def test_empty_string_role_defaults_to_family_dashboard(self):
        request = self._make_request(role='')
        url = RoleAwareAccountAdapter(request).get_login_redirect_url(request)
        assert url == '/family/dashboard/'

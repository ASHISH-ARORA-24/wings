import pytest
from django.test import RequestFactory

from wings.context_processors import site_name


@pytest.mark.django_db
class TestSiteNameContextProcessor:

    def test_returns_site_name_key(self, settings):
        settings.SITE_NAME = 'Test Site'
        factory = RequestFactory()
        request = factory.get('/')
        result = site_name(request)
        assert 'site_name' in result

    def test_site_name_value_matches_settings(self, settings):
        settings.SITE_NAME = 'Wing Man'
        factory = RequestFactory()
        request = factory.get('/')
        result = site_name(request)
        assert result['site_name'] == 'Wing Man'

    def test_site_name_reflects_settings_change(self, settings):
        settings.SITE_NAME = 'New Name'
        factory = RequestFactory()
        request = factory.get('/')
        result = site_name(request)
        assert result['site_name'] == 'New Name'

import pytest
from model_bakery import baker

from accounts.models import UserExtraInfo


@pytest.mark.django_db
class TestUserExtraInfoModel:

    def test_role_constants(self):
        assert UserExtraInfo.FAMILY == 'family'
        assert UserExtraInfo.VENDOR == 'vendor'

    def test_role_choices_contains_family_and_vendor(self):
        values = [choice[0] for choice in UserExtraInfo.ROLE_CHOICES]
        assert 'family' in values
        assert 'vendor' in values

    def test_str_returns_username(self):
        extra = baker.make(UserExtraInfo)
        assert str(extra) == extra.user.username

    def test_phone_is_optional(self):
        extra = baker.make(UserExtraInfo, phone='')
        assert extra.phone == ''

    def test_role_is_optional(self):
        extra = baker.make(UserExtraInfo, role='')
        assert extra.role == ''

    def test_family_role(self):
        extra = baker.make(UserExtraInfo, role=UserExtraInfo.FAMILY)
        assert extra.role == 'family'

    def test_vendor_role(self):
        extra = baker.make(UserExtraInfo, role=UserExtraInfo.VENDOR)
        assert extra.role == 'vendor'

    def test_one_to_one_link(self):
        extra = baker.make(UserExtraInfo)
        assert extra.user.extra_info == extra

    def test_deleting_user_deletes_extra_info(self):
        extra = baker.make(UserExtraInfo)
        user_id = extra.user.id
        extra.user.delete()
        assert not UserExtraInfo.objects.filter(user_id=user_id).exists()

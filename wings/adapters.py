from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class RoleAwareAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        role = request.session.get('login_role')
        if role == 'vendor':
            return '/vendor/dashboard/'
        return '/family/dashboard/'


class RoleAwareSocialAccountAdapter(DefaultSocialAccountAdapter):
    pass

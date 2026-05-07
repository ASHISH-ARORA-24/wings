from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserExtraInfo


class UserExtraInfoInline(admin.StackedInline):
    model = UserExtraInfo
    can_delete = False
    verbose_name_plural = 'Extra Info'


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserExtraInfoInline]

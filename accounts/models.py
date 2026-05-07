from django.contrib.auth.models import User
from django.db import models


class UserExtraInfo(models.Model):
    FAMILY = 'family'
    VENDOR = 'vendor'
    ROLE_CHOICES = [
        (FAMILY, 'Family'),
        (VENDOR, 'Vendor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra_info')
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True)

    class Meta:
        verbose_name = 'User Extra Info'
        verbose_name_plural = 'User Extra Info'

    def __str__(self):
        return self.user.username

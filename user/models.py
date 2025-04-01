from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True, unique=True)
    country = CountryField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        permissions = [
            ("can_block_users", "Может блокировать пользователей")
        ]

    def __str__(self):
        return self.email

    def is_manager(self):
        return self.groups.filter(name="Менеджеры").exists()

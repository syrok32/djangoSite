from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True)  # Делаем email обязательным
    is_blocked = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)  # Флаг подтверждения email
    USERNAME_FIELD = "email"  # Теперь логин через email
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email


    def is_manager(self):
        return self.groups.filter(name="Менеджеры").exists()
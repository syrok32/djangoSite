from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Делаем email обязательным
    is_blocked = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)  # Флаг подтверждения email

    def __str__(self):
        return self.username

    def is_manager(self):
        return self.groups.filter(name="Менеджеры").exists()
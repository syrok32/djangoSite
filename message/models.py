from django.db import models

from user.models import CustomUser


# Create your models here.
class  Message(models.Model):
    theme = models.CharField(max_length=80, verbose_name="Тема письма")
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages", verbose_name="Владелец")



    class Meta():
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['theme']
        permissions = [
            ("can_manage_messages", "Может управлять сообщениями"),
        ]

    def __str__(self):
        return f'{self.theme}'
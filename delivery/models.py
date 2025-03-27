# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

from distribution.models import Distribution


class Delivery(models.Model):

    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("faile", "Не успешно"),
    ]

    distribution = models.ForeignKey("distribution.Distribution", on_delete=models.CASCADE, verbose_name="Рассылка")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)

    def __str__(self):
        return f"Попытка {self.pk} - {self.get_status_display()}"


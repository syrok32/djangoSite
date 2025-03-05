import psycopg
from django.db import models

# Create your models here.
from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(max_length=40, unique=True, blank=True, verbose_name='Введите почту')
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    comment = models.TextField(verbose_name='коментарийучше')

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылки"
        ordering = ['name']

    def __str__(self):
        return f"{self.email}"

from django.db import models

# Create your models here.
class  Message(models.Model):
    theme = models.CharField(max_length=80, verbose_name="Тема письма")
    body = models.TextField(verbose_name='Тело письма')



    class Meta():
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['theme']

    def __str__(self):
        return f'{self.theme}'
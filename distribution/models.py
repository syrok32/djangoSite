from django.db import models

import user
from message.models import Message
from newsletter_recipient.models import Newsletter
from user.models import CustomUser

# Create your models here.
PROSESS_CHOICES = {
    "compl": "Завепшена",
    "create": "Создана",
    "start": "Запущена",
}


class Distribution(models.Model):
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Вреимя окончания")
    state = models.CharField(max_length=20, choices=PROSESS_CHOICES, null=False, verbose_name="статус")
    message_distribution = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="Сообщение")
    recipients = models.ManyToManyField(Newsletter)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="distributions", verbose_name="Владелец")

    def start_sending(self):
        """Метод для отправки рассылки по требованию."""
        from django.core.mail import send_mail
        try:
            for recipient in self.recipients.all():
                send_mail(
                    self.message_distribution.subject,
                    self.message_distribution.body,
                    'from@example.com',  # Отправитель
                    [recipient.email],
                    fail_silently=False,
                )
            self.status = 'start'  # Обновляем статус
            self.save()
            return "Рассылка успешно отправлена"
        except Exception as e:
            return f"Ошибка отправки рассылки: {str(e)}"

from django.core.mail import send_mail
from django.db import models


from message.models import Message
from newsletter_recipient.models import Newsletter
from user.models import CustomUser


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
    recipients = models.ManyToManyField(Newsletter, blank=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="distributions", verbose_name="Владелец")

    def start_sending(self):
        from delivery.models import Delivery
        """Метод для отправки рассылки по требованию."""
        success_count = 0
        failure_count = 0
        error_messages = []

        for recipient in self.recipients.all():
            try:
                send_mail(
                    self.message_distribution.theme,
                    self.message_distribution.body,
                    'stepstepan2@gmail.com',  # Отправитель
                    [recipient.email],
                    fail_silently=False,
                )
                success_count += 1

                # Создаём запись в Delivery о успешной попытке
                Delivery.objects.create(
                    distribution=self,
                    status="success",
                    response="Email успешно отправлен"
                )

            except Exception as e:
                failure_count += 1
                error_messages.append(f"Ошибка при отправке на {recipient.email}: {str(e)}")

                # Создаём запись в Delivery о неудачной попытке
                Delivery.objects.create(
                    distribution=self,
                    status="faile",
                    response=str(e)
                )

        # Обновляем статус рассылки
        if success_count > 0:
            self.state = 'start'
            self.save()

        return f"Рассылка завершена: {success_count} успешно, {failure_count} неуспешно."
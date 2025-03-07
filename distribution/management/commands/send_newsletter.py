from django.core.management.base import BaseCommand
from distribution.models import Distribution, DeliveryAttempt
from django.utils.timezone import now
import smtplib


class Command(BaseCommand):
    help = "Отправка сообщений по рассылке"

    def handle(self, *args, **kwargs):
        distributions = Distribution.objects.filter(status="created", start_time__lte=now())

        for distribution in distributions:
            for recipient in distribution.recipients.all():
                try:

                    print(f"Отправка сообщения '{distribution.message.subject}' на {recipient.email}")

                    # Логируем успешную попытку
                    DeliveryAttempt.objects.create(
                        distribution=distribution,
                        status="success",
                        response="Email sent successfully"
                    )
                except Exception as e:

                    DeliveryAttempt.objects.create(
                        distribution=distribution,
                        status="failed",
                        response=str(e)
                    )


            distribution.status = "running"
            distribution.save()

        self.stdout.write("Рассылки отправлены")

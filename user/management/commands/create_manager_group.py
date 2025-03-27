from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from user.models import CustomUser

class Command(BaseCommand):
    help = "Создает группу 'Менеджеры' с нужными правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Managers")
        permissions = Permission.objects.filter(
            codename__in=["can_manage_newsletters", "can_manage_messages"]
        )
        group.permissions.set(permissions)
        group.save()

        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана и права добавлены."))

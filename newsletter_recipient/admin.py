from django.contrib import admin

from newsletter_recipient.models import Newsletter


# Register your models here.
@admin.register(Newsletter)
class Newsletter_recipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'email')




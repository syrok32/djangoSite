from django.contrib import admin

from delivery.models import Delivery


# Register your models here.
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass
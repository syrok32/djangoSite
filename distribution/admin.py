from django.contrib import admin

from distribution.models import Distribution


# Register your models here.


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    pass
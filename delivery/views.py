
from django.shortcuts import render
from django.views.generic import ListView
from delivery.models import Delivery


# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView
from delivery.models import Delivery


# Create your views here.
from django.views.generic import ListView
from .models import Delivery

class DeliveryListView(ListView):
    model = Delivery
    template_name = 'delivery/delivery_list.html'
    context_object_name = 'delivery_attempts'

    def get_queryset(self):
        """Фильтруем попытки по конкретной рассылке, если передан ID."""
        distribution_id = self.kwargs.get('distribution_id')
        if distribution_id:
            return Delivery.objects.filter(distribution_id=distribution_id)
        return Delivery.objects.all()

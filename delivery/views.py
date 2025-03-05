
from django.shortcuts import render
from django.views.generic import ListView
from delivery.models import Delivery


# Create your views here.
class DeliveryListView(ListView):
    model = Delivery
    template_name = 'delivery/delivery_list.html'
    # для доступа к попыткам рассылки в шаблоне


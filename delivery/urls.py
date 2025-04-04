from django.urls import path

from .views import DeliveryListView

urlpatterns = [
    path('delivery_attempts/', DeliveryListView.as_view(), name="delivery_attempt_list"),
    path('delivery/<int:distribution_id>/', DeliveryListView.as_view(), name='delivery-list-filtered'),
]

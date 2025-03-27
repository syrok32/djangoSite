from django.urls import path

from . import views
from .views import DistributionListView, DistributionDetailView, DistributionCreateView, DistributionDeleteView, \
    DistributionSendView, DistributionUpdateView

app_name = "distribution"

urlpatterns = [
    path('list', DistributionListView.as_view(), name="distribution_list"),
    path('detail/<int:pk>', DistributionDetailView.as_view(), name="distribution_detail"),
    path('create', DistributionCreateView.as_view(), name='distribution_create'),
    path('delete/<int:pk>', DistributionDeleteView.as_view(), name='distribution_delete'),
    path('send/<int:pk>/', DistributionSendView.as_view(), name='distribution_send'),
    path('<int:pk>/update/', DistributionUpdateView.as_view(), name='distribution_update'),
    path('distributions/<int:pk>/send/', views.DistributionSendView.as_view(), name='distribution_send')
]

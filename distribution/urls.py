from django.urls import path

from .views import DistributionListView, DistributionDetailView, DistributionCreateView, DistributionDeleteView, \
    DistributionSendView, HomeView

app_name = "distribution"

urlpatterns = [
    path('', DistributionListView.as_view(), name="distribution_list"),
    path('detail/<int:pk>', DistributionDetailView.as_view(), name="distribution_detail"),
    path('create', DistributionCreateView.as_view(), name='distribution_create'),
    path('delete/<int:pk>', DistributionDeleteView.as_view(), name='distribution_delete'),
    path('send/<int:pk>/', DistributionSendView.as_view(), name='distribution_send'),
    path('home', HomeView.as_view(), name='home')
]

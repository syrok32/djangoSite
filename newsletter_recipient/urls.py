from django.urls import path
from django.urls import path
from .views import (
    NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView,

)

urlpatterns = [

    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter/<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletter_delete')


]
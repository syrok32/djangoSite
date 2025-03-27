from django.urls import path
from .views import (
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView
)

urlpatterns = [

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete')
]
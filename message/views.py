from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Message


# Список всех сообщений
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


# Детали конкретного сообщения
class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'
    context_object_name = 'message'



# Создание нового сообщения
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'message/message_form.html'
    fields = ['theme', 'body']
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



# Редактирование сообщения
class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'message/message_form.html'
    fields = ['theme', 'body']
    success_url = reverse_lazy('message_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)


# Удаление сообщения
class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)

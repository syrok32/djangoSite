from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Newsletter
# Create your views here.

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Newsletter


# Список всех подписчиков
class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        return Newsletter.objects.filter(owner=self.request.user)


# Детали конкретного подписчика
class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter/newsletter_detail.html'
    context_object_name = 'newsletter'


# Создание нового подписчика
class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    template_name = 'newsletter/newsletter_form.html'
    fields = ['email', 'name', 'surname', 'patronymic', 'comment']
    success_url = reverse_lazy('newsletter_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Редактирование подписчика
class NewsletterUpdateView(UpdateView):
    model = Newsletter
    template_name = 'newsletter/newsletter_form.html'
    fields = ['email', 'name', 'surname', 'patronymic', 'comment']
    success_url = reverse_lazy('newsletter_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)


# Удаление подписчика
class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletter/newsletter_confirm_delete.html'
    success_url = reverse_lazy('newsletter_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)
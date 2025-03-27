from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, CreateView, DeleteView, TemplateView, View, UpdateView

from newsletter_recipient.models import Newsletter
from .forms import DistributionForm
from .models import Distribution

@method_decorator(cache_page(60 * 15), name='dispatch')
class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution
    template_name = "distribution/distributionList.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Managers').exists():
            return Distribution.objects.all()
        return Distribution.objects.filter(owner=user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class DistributionDetailView(LoginRequiredMixin, DetailView):
    model = Distribution
    template_name = "distribution/distributionDetail.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class DistributionCreateView(LoginRequiredMixin, CreateView):
    model = Distribution
    template_name = 'distribution/distributionCreate.html'
    form_class = DistributionForm
    success_url = reverse_lazy('distribution:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class DistributionDeleteView(LoginRequiredMixin, DeleteView):
    model = Distribution
    template_name = 'distribution/distributionDelete.html'
    success_url = reverse_lazy('distribution:distribution_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет прав на удаление этой рассылки.")
        return super().dispatch(request, *args, **kwargs)



class DistributionSendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(Distribution, pk=self.kwargs['pk'])
        if obj.owner != request.user and not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет доступа!")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        distribution = get_object_or_404(Distribution, pk=pk)
        result = distribution.start_sending()
        return HttpResponse(result)

@method_decorator(cache_page(60 * 15), name='dispatch')
class HomeView(TemplateView):
    template_name = 'distribution/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_distributions'] = Distribution.objects.all().count()
        context['active_distributions'] = Distribution.objects.filter(state='start').count()
        context['unique_recipients'] = Newsletter.objects.all().distinct().count()
        return context
@method_decorator(cache_page(60 * 15), name='dispatch')
class DistributionUpdateView(LoginRequiredMixin, UpdateView):
    model = Distribution
    template_name = 'distribution/distributionUpdate.html'  # создайте шаблон для обновления
    form_class = DistributionForm
    success_url = reverse_lazy('distribution:distribution_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав доступа
        if obj.owner != request.user and not request.user.groups.filter(name="Managers").exists():
            return HttpResponseForbidden("У вас нет прав на редактирование этой рассылки.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Здесь можно добавить дополнительную логику перед сохранением
        return super().form_valid(form)
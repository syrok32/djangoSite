from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, CreateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

from distribution.models import Distribution
from newsletter_recipient.models import Newsletter
from .forms import DistributionForm
@cache_page(60 * 15)
class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution
    template_name = "distribution/distributionList.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Managers').exists():
            # Менеджеры видят все рассылки
            return Distribution.objects.all()
        # Обычные пользователи видят только свои рассылки
        return Distribution.objects.filter(owner=user)

@cache_page(60 * 15)
class DistributionDetailView(LoginRequiredMixin, DetailView):
    model = Distribution
    template_name = "distribution/distributionDetail.html"

    def test_func(self):
        user = self.request.user
        distribution = self.get_object()
        # Менеджеры могут смотреть все рассылки, или если пользователь является владельцем
        return user.groups.filter(name='Managers').exists() or distribution.owner == user

@cache_page(60 * 15)
class DistributionCreateView(LoginRequiredMixin, CreateView):
    model = Distribution
    template_name = 'distribution/distributionCreate.html'
    form_class = DistributionForm
    success_url = reverse_lazy('distribution:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@cache_page(60 * 15)
class DistributionDeleteView(LoginRequiredMixin, DeleteView):
    model = Distribution
    template_name = 'distribution/distributionDelete.html'
    success_url = reverse_lazy('distribution:distribution_list')

    def get_object(self, queryset=None):
        """Переопределение метода get_object для проверки владельца."""
        obj = super().get_object(queryset)
        # Проверяем, что пользователь является владельцем рассылки или менеджером
        if obj.owner != self.request.user and not self.request.user.groups.filter(name='Managers').exists():
            raise HttpResponseForbidden("У вас нет прав на удаление этой рассылки.")
        return obj

@cache_page(60 * 15)
class DistributionSendView(LoginRequiredMixin, View):
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

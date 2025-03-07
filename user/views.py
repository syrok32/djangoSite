

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView

from distribution.models import Distribution
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import CustomUser

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"http://127.0.0.1:8000/user/verify/{uid}/{token}/"

        send_mail(
            'Подтвердите свой email',
            f'Пройдите по ссылке для подтверждения: {verification_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return response
    def test_func(self):
        return self.request.user.groups.filter(name='Managers').exists()

class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user/user_list.html'

    def get_queryset(self):
        # Здесь можно добавить логику для фильтрации пользователей, если нужно
        return CustomUser.objects.all()

    def test_func(self):
        # Проверяем, является ли пользователь менеджером
        if not self.request.user.groups.filter(name='Manager').exists():
            raise HttpResponseForbidden("У вас нет прав для просмотра списка пользователей.")
        return True


class BlockUserView(View):
    def post(self, request, user_id):
        if not request.user.groups.filter(name='Managers').exists():
            return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")

        user = CustomUser.objects.get(id=user_id)
        user.is_blocked = True
        user.save()
        return redirect('user_list')  # Название URL для списк


class StopDistributionView(View):
    def post(self, request, pk):
        if not request.user.groups.filter(name='Managers').exists():
            return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")

        distribution = get_object_or_404(Distribution, pk=pk)
        distribution.state = 'stopped'
        distribution.save()
        return redirect('distribution:distribution_list')  # Название URL для списка рассылок

class CustomLogoutView(LogoutView):

    template_name = 'user/logout.html'
    next_page = reverse_lazy('login')
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('distribution:home')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return HttpResponse("Email подтверждён! Теперь вы можете войти.")
    return HttpResponse("Недействительная ссылка верификации.")


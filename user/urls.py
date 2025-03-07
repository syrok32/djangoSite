from django.contrib.auth import views as auth_views
from django.urls import path

from .views import RegisterView, verify_email, CustomLoginView, CustomLogoutView, UserListView, BlockUserView, \
    StopDistributionView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('stop_distribution/<int:pk>/', StopDistributionView.as_view(), name='stop_distribution'),

]

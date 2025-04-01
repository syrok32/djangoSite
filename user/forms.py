
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'country',  'phone_number', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'country',  'phone_number', 'email', 'first_name', 'last_name']

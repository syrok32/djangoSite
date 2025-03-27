# forms.py
from django import forms
from .models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'country',  'phone_number', 'email', 'first_name', 'last_name'] # Включаем только необходимые поля для редактирования

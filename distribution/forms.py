from django import forms
from .models import Distribution

class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['start_time', 'end_time', 'message_distribution', 'recipients']  # Поле `state` заполняется автоматически
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message_distribution': forms.Select(attrs={'class': 'form-select'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.state = 'create'  # Устанавливаем статус "Создана" автоматически

        if commit:
            instance.save()
            self.save_m2m()  # Сохраняем ManyToMany поле recipients

        return instance

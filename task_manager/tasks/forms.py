from django import forms
from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }

        widgets = {
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True,
                }
            ),
            'executor': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'labels': forms.SelectMultiple(
                attrs={
                    'class': 'form-select',
                }
            ),
        }

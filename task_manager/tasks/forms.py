from django import forms

from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['name', 'description', 'status', 'executor']

        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
        }
        status = forms.ChoiceField(initial='---------',
                                   widget=forms.Select(
                                       attrs={
                                           'required': True,
                                           'size': 2,
                                       }
                                   ))
        executor = forms.ChoiceField(initial='---------',
                                     widget=forms.Select(
                                         attrs={'size': 10}
                                     ))

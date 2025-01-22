from django import forms

from .models import Task
from task_manager.users.models import User

class TaskCreateForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label_set']

        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'label_set': 'Метки',
        }
        status = forms.ChoiceField(initial='---------',
                                   widget=forms.Select(
                                       attrs={
                                           'required': True,
                                           'size': 2,
                                       }
                                   ))
        executor = forms.ModelChoiceField(queryset=User.objects.all(),
                                          widget=forms.Select(attrs={
                                              'size': 10
                                              }),
                                          empty_label='---------',
                                        )
        label_set = forms.MultipleChoiceField()

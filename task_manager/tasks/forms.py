from django import forms

from task_manager.users.models import User

from .models import Task


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.get_full_name()}'


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
        executor = CustomChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
        )
        label_set = forms.MultipleChoiceField()

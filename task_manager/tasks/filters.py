import django_filters
from django import forms
from django_filters import BooleanFilter, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        required=False,
        empty_label='---------',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        required=False,
        empty_label='---------',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    label_set = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        required=False,
        empty_label='---------',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    self_tasks = BooleanFilter(
        field_name='author',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Только свои задачи',
        method='self_own_tasks'
    )

    def self_own_tasks(self, queryset, self_tasks, value):
        if not value:
            return queryset
        return queryset.filter(author=self.request.user)

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label_set', 'self_tasks']

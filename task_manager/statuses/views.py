from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Status
from .forms import StatusCreateForm
from task_manager.mixins import LoginPermissionRequiredMixin


class IndexView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'status_list.html'


class StatusCreateView(LoginPermissionRequiredMixin, SuccessMessageMixin,
                       LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'status_create.html'
    form_class = StatusCreateForm
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно создан'


class StatusUpdateView(LoginPermissionRequiredMixin, SuccessMessageMixin,
                       LoginRequiredMixin, UpdateView):
    model = Status
    context_object_name = 'status'
    template_name = 'status_update.html'
    form_class = StatusCreateForm
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно изменен'


class StatusDeleteView(LoginPermissionRequiredMixin, SuccessMessageMixin,
                       LoginRequiredMixin, DeleteView):
    model = Status
    context_object_name = 'status'
    template_name = 'status_delete.html'
    success_url = reverse_lazy('status_list')
    reject_url = reverse_lazy('status_list')
    success_message = 'Статус успешно удален'
    reject_message = 'Невозможно удалить статус, потому что он используется'
    
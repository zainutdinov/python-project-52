from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import DeletionRestricted, LoginPermissionRequiredMixin

from .forms import LabelCreateForm
from .models import Label


class IndexView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels_list.html'


class LabelCreateView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels_create.html'
    form_class = LabelCreateForm
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно создана'


class LabelUpdateView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = Label
    context_object_name = 'label'
    template_name = 'labels_update.html'
    form_class = LabelCreateForm
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                      SuccessMessageMixin, DeletionRestricted, DeleteView):
    model = Label
    context_object_name = 'label'
    template_name = 'labels_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = 'Метка успешно удалена'

    reject_url = reverse_lazy('labels_list')
    reject_message = 'Невозможно удалить метку, потому что она используется'

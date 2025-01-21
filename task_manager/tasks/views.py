from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from task_manager.mixins import LoginPermissionRequiredMixin

from .filters import TaskFilter
from .forms import TaskCreateForm
from .mixins import AuthorRequiredMixin
from .models import Task


class IndexView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                FilterView, ListView):
    model = Task
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     DetailView):
    model = Task
    template_name = 'tasks_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks_create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    context_object_name = 'task'
    template_name = 'tasks_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                     SuccessMessageMixin, AuthorRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'

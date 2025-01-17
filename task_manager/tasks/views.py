from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import TaskCreateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginPermissionRequiredMixin
from .mixins import AuthorRequiredMixin



class IndexView(LoginPermissionRequiredMixin, LoginRequiredMixin,
                ListView):
    model = Task
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'


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


class TaskDeleteView(AuthorRequiredMixin, LoginPermissionRequiredMixin, 
                     LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import DeletionRestricted, LoginPermissionRequiredMixin

from .forms import UserCreateForm, UserUpdateForm
from .mixins import UserPermissionRequiredMixin
from .models import User


class IndexView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(LoginPermissionRequiredMixin, UserPermissionRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users_update.html'
    success_url = reverse_lazy('users_list')
    initial = {'password': ''}
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(LoginPermissionRequiredMixin, UserPermissionRequiredMixin,
                     SuccessMessageMixin, DeletionRestricted, DeleteView):
    model = User
    template_name = 'users_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'

    reject_url = reverse_lazy('users_list')
    reject_message = ('Невозможно удалить пользователя, '
                      'потому что он используется')

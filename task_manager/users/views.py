from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

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


class UserUpdateView(UserPermissionRequiredMixin, SuccessMessageMixin,
                     LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users_update.html'
    success_url = reverse_lazy('users_list')
    initial = {'password': ''}
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(UserPermissionRequiredMixin, SuccessMessageMixin,
                     LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'

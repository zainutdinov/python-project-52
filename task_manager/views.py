from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    success_message = 'Вы залогинены'


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    next_page = 'home'
    success_message = 'Вы разлогинены'

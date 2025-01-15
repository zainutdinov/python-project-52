from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class LoginPermissionRequiredMixin:
    """
    Миксин для проверки авторизации.
    """
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
                extra_tags="danger"
            )
            return HttpResponseRedirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
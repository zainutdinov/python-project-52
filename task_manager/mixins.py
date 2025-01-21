from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class LoginPermissionRequiredMixin(LoginRequiredMixin):
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
    

class DeletionRestricted:
    """
    Миксин для проверки, что обьект не используется и обработки исключения,
    если обьект используется и его невозможно удалить.
    """
    reject_message = None
    reject_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.reject_message, extra_tags="danger")
            return HttpResponseRedirect(self.reject_url)
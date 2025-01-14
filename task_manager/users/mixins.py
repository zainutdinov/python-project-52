from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class UserPermissionRequiredMixin:
    """
    Миксин для проверки прав на редактирование или удаление пользователей.
    """
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        user_to_process = self.get_object()
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
                extra_tags="danger"
            )
            return HttpResponseRedirect(self.login_url)
        if user_to_process != request.user:
            messages.error(
                request,
                "У вас нет прав для изменения другого пользователя.",
                extra_tags="danger"
            )
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
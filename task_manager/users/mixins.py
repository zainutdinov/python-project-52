from django.contrib import messages
from django.http import HttpResponseRedirect


class UserPermissionRequiredMixin:
    """
    Миксин для проверки прав на редактирование или удаление пользователей.
    """
    
    def dispatch(self, request, *args, **kwargs):
        user_to_process = self.get_object()
        if user_to_process != request.user:
            messages.error(
                request,
                "У вас нет прав для изменения другого пользователя.",
                extra_tags="danger"
            )
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
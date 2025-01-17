from django.contrib import messages
from django.http import HttpResponseRedirect


class AuthorRequiredMixin:
    """
    Миксин для проверки, что текущий пользователь является автором задачи.
    """
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, "Только автор может удалить эту задачу.", 
                           extra_tags="danger")
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

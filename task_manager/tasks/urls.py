from django.urls import path

from .views import (
                    IndexView,
                    TaskCreateView,
                    TaskDeleteView,
                    TaskDetailView,
                    TaskUpdateView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='tasks_detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='tasks_delete')
]

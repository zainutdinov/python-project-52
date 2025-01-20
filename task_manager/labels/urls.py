from django.urls import path

from .views import (
                    IndexView,
                    LabelCreateView,
                    LabelDeleteView,
                    LabelUpdateView,
                    )

urlpatterns = [
    path('', IndexView.as_view(), name='labels_list'),
    path('create/', LabelCreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='labels_delete')
]

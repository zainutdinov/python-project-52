from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), 
         name='users_list'),
    path('create/', views.UserCreateView.as_view(),
         name='users_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(),
         name='users_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(),
         name='users_delete')
]

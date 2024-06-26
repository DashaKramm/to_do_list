from django.urls import path

from webapp.views import index, create_task, delete_task, detailed_task_view

urlpatterns = [
    path('', index, name='tasks'),
    path('create/', create_task, name='create_task'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('task/<int:pk>/', detailed_task_view, name='detailed_task_view'),
]

from django.urls import path

from webapp.views import index, create_task, delete_task, detailed_task_view

urlpatterns = [
    path('', index),
    path('create/', create_task),
    path('delete/<int:pk>/', delete_task),
    path('task/<int:pk>/', detailed_task_view),
]

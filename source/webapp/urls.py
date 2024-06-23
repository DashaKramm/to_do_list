from django.urls import path

from webapp.views import index, create_task, delete_task

urlpatterns = [
    path('', index),
    path('create/', create_task),
    path('delete/', delete_task),
]

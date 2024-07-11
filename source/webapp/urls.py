from django.urls import path

from webapp.views import TaskListView, TaskDetailView, CreateTaskView, UpdateTaskView, DeleteTaskView, \
    TasksListDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('task/<int:pk>/delete', DeleteTaskView.as_view(), name='delete_task'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='detailed_task_view'),
    path('task/<int:pk>/update', UpdateTaskView.as_view(), name='update_task'),
    path('tasks/', TasksListDeleteView.as_view(), name='tasks_list'),
]

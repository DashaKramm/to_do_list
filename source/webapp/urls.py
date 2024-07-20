from django.urls import path
from django.views.generic import RedirectView

from webapp.views import TaskDetailView, UpdateTaskView, DeleteTaskView, TasksListDeleteView, ProjectListView, \
    CreateProjectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='projects')),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('task/<int:pk>/delete', DeleteTaskView.as_view(), name='delete_task'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='detailed_task_view'),
    path('task/<int:pk>/update', UpdateTaskView.as_view(), name='update_task'),
    path('tasks_multiple_delete/', TasksListDeleteView.as_view(), name='tasks_list'),
]

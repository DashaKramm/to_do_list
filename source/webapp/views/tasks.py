from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView

from webapp.forms import TaskForm, TaskDeleteForm
from webapp.models import Task, Project


# Create your views here.
class CreateTaskView(PermissionRequiredMixin, CreateView):
    template_name = "tasks/create_task.html"
    form_class = TaskForm
    permission_required = "webapp.add_task"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect(project.get_absolute_url())


class DeleteTaskView(PermissionRequiredMixin, DeleteView):
    template_name = "tasks/delete_task.html"
    model = Task
    permission_required = "webapp.delete_task"

    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and task.project.users.filter(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("webapp:detailed_project_view", kwargs={"pk": self.object.project.pk})


class TaskDetailView(DetailView):
    template_name = "tasks/detailed_task_view.html"
    model = Task

    def get_object(self, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'), is_deleted=False)
        return task


class UpdateTaskView(PermissionRequiredMixin, UpdateView):
    template_name = "tasks/update_task.html"
    form_class = TaskForm
    model = Task
    permission_required = "webapp.change_task"

    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and task.project.users.filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse("webapp:detailed_project_view", kwargs={"pk": self.object.project.pk})


class TasksListDeleteView(PermissionRequiredMixin, TemplateView):
    template_name = 'tasks/tasks_list.html'
    permission_required = "webapp.delete_task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tasks'] = Task.objects.order_by('-id')
        context['form'] = TaskDeleteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskDeleteForm(data=request.POST)
        if form.is_valid():
            delete_tasks = form.cleaned_data['tasks']
            delete_tasks.delete()
            return redirect('webapp:projects')
        return render(request, self.template_name, context={'form': form})

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView

from webapp.forms import TaskForm, TaskDeleteForm
from webapp.models import Task, Project


# Create your views here.
class CreateTaskView(CreateView):
    template_name = "tasks/create_task.html"
    form_class = TaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect(project.get_absolute_url())


class DeleteTaskView(DeleteView):
    template_name = "tasks/delete_task.html"
    model = Task

    def get_success_url(self):
        return reverse_lazy("detailed_project_view", kwargs={"pk": self.object.project.pk})


class TaskDetailView(DetailView):
    template_name = "tasks/detailed_task_view.html"
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['task'] = self.object
        return context


class UpdateTaskView(UpdateView):
    template_name = "tasks/update_task.html"
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse("detailed_project_view", kwargs={"pk": self.object.project.pk})


class TasksListDeleteView(TemplateView):
    template_name = 'tasks/tasks_list.html'

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
            return redirect('projects')
        return render(request, self.template_name, context={'form': form})

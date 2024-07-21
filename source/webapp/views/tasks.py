from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

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


class DeleteTaskView(TemplateView):
    template_name = "tasks/delete_task.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['task'] = self.task
        return context

    def post(self, request, *args, **kwargs):
        self.task.delete()
        return HttpResponseRedirect(reverse('projects'))


class TaskDetailView(TemplateView):
    template_name = "tasks/detailed_task_view.html"

    def get_context_data(self, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        context = super().get_context_data()
        context['task'] = task
        return context


class UpdateTaskView(TemplateView):
    template_name = "tasks/update_task.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = TaskForm(instance=self.task)
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST, instance=self.task)
        if form.is_valid():
            self.task = form.save()
            return redirect('detailed_task_view', pk=self.task.pk)
        return render(request, self.template_name, context={'form': form})


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

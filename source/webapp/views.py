from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from webapp.forms import TaskForm, TaskDeleteForm
from webapp.models import Task


# Create your views here.
class TaskListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tasks'] = Task.objects.order_by('-id')
        return context


class CreateTaskView(TemplateView):
    template_name = "create_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('detailed_task_view', pk=task.pk)
        return render(request, self.template_name, context={'form': form})


class DeleteTaskView(TemplateView):
    template_name = "delete_task.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['task'] = self.task
        return context

    def post(self, request, *args, **kwargs):
        self.task.delete()
        return HttpResponseRedirect(reverse('tasks'))


class TaskDetailView(TemplateView):
    template_name = "detailed_task_view.html"

    def get_context_data(self, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        context = super().get_context_data()
        context['task'] = task
        return context


class UpdateTaskView(TemplateView):
    template_name = "update_task.html"

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
    template_name = 'tasks_list.html'

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
            return redirect('tasks')
        return render(request, self.template_name, context={'form': form})

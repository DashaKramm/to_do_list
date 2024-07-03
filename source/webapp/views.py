from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.forms import TaskForm, TaskDeleteForm
from webapp.models import Task


# Create your views here.
def index(request):
    tasks = Task.objects.order_by('-id')
    return render(request, 'index.html', context={'tasks': tasks})


def create_task(request):
    if request.method == "GET":
        form = TaskForm()
        return render(request, "create_task.html", context={'form': form})
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('detailed_task_view', pk=task.pk)
        return render(request, "create_task.html", context={'form': form})


def delete_task(request, *args, pk, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        return render(request, "delete_task.html", context={"task": task})
    else:
        task.delete()
        return HttpResponseRedirect(reverse('tasks'))


def detailed_task_view(request, *args, pk, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "detailed_task_view.html", context={"task": task})


def update_task(request, *args, pk, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        form = TaskForm(instance=task)
        return render(request, "update_task.html", context={'form': form})
    else:
        form = TaskForm(data=request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('detailed_task_view', pk=task.pk)
        else:
            return render(request, "update_task.html", context={'form': form})


def tasks_list(request):
    tasks = Task.objects.order_by('-id')
    if request.method == "GET":
        form = TaskDeleteForm()
        return render(request, 'tasks_list.html', context={'form': form, 'tasks': tasks})
    else:
        form = TaskDeleteForm(data=request.POST)
        if form.is_valid():
            delete_tasks = form.cleaned_data['tasks']
            delete_tasks.delete()
            return redirect('tasks')
        return render(request, 'tasks_list.html', context={'form': form, 'tasks': tasks})

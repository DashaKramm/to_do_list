from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Task, status_choices


# Create your views here.
def index(request):
    tasks = Task.objects.order_by('-id')
    return render(request, 'index.html', context={'tasks': tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", context={'status_choices': status_choices})
    else:
        description = request.POST.get("description")
        status = request.POST.get("status")
        date_of_completion = request.POST.get("date_of_completion")
        detailed_description = request.POST.get("detailed_description")
        if not date_of_completion:
            date_of_completion = None
        task = Task.objects.create(
            description=description,
            status=status,
            date_of_completion=date_of_completion,
            detailed_description=detailed_description,
        )
        return redirect('detailed_task_view', pk=task.pk)


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
        return render(request, "update_task.html", context={
            'status_choices': status_choices,
            'task': get_object_or_404(Task, pk=pk)
        })
    else:
        task.description = request.POST.get("description")
        task.status = request.POST.get("status")
        task.date_of_completion = request.POST.get("date_of_completion") or None
        task.detailed_description = request.POST.get("detailed_description")
        task.save()
        return redirect('detailed_task_view', pk=task.pk)

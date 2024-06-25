from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

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
        Task.objects.create(
            description=description,
            status=status,
            date_of_completion=date_of_completion,
            detailed_description=detailed_description,
        )
        return HttpResponseRedirect("/")


def delete_task(request, *args, pk, **kwargs):
    get_object_or_404(Task, pk=pk).delete()
    return HttpResponseRedirect("/")

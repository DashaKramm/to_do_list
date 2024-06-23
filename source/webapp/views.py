from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.models import Task, status_choices


# Create your views here.
def index(request):
    tasks = Task.objects.order_by('-id')
    return render(request, 'index.html', context={'tasks': tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", context={'status_choices': status_choices})
    else:
        Task.objects.create(
            description=request.POST.get("description"),
            status=request.POST.get("status"),
            date_of_completion=request.POST.get("date_of_completion")
        )
        return HttpResponseRedirect("/")

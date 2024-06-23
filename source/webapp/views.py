from django.shortcuts import render

from webapp.models import Task


# Create your views here.
def index(request):
    tasks = Task.objects.order_by('-id')
    return render(request, 'index.html', context={'tasks': tasks})

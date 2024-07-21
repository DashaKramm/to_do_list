from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView

from webapp.forms import SearchForm
from webapp.forms.projects import ProjectForm
from webapp.models import Project, Task


# Create your views here.
class ProjectListView(ListView):
    template_name = 'projects/index.html'
    model = Project
    context_object_name = 'projects'
    ordering = ['-end_date', '-start_date']
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(name__contains=self.search_value) | Q(description__contains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class CreateProjectView(CreateView):
    template_name = "projects/create_project.html"
    form_class = ProjectForm


class ProjectDetailView(DetailView):
    template_name = "projects/detailed_project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object).order_by('-id')
        return context

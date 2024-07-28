from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import SearchForm, ProjectUserForm
from webapp.forms.projects import ProjectForm
from webapp.models import Project, Task


# Create your views here.
class ProjectListView(ListView):
    template_name = 'projects/index.html'
    model = Project
    context_object_name = 'projects'
    ordering = ['end_date', 'start_date']
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
        projects = context['projects']
        user = self.request.user
        for project in projects:
            project.is_user = project.users.filter(pk=user.pk)
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class CreateProjectView(PermissionRequiredMixin, CreateView):
    template_name = "projects/create_project.html"
    form_class = ProjectForm
    permission_required = "webapp.add_project"

    def form_valid(self, form):
        self.object.users.add(self.request.user)
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    template_name = "projects/detailed_project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['tasks'] = Task.objects.filter(project=self.object, is_deleted=False).order_by('-id')
        context['is_user'] = project.users.filter(pk=self.request.user.pk)
        return context


class UpdateProjectView(PermissionRequiredMixin, UpdateView):
    template_name = "projects/update_project.html"
    form_class = ProjectForm
    model = Project
    permission_required = "webapp.change_project"

    def has_permission(self):
        project = self.get_object()
        return super().has_permission() and project.users.filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse("webapp:detailed_project_view", kwargs={"pk": self.object.pk})


class DeleteProjectView(PermissionRequiredMixin, DeleteView):
    template_name = "projects/delete_project.html"
    model = Project
    success_url = reverse_lazy("webapp:projects")
    permission_required = "webapp.delete_project"

    def has_permission(self):
        project = self.get_object()
        return super().has_permission() and project.users.filter(pk=self.request.user.pk)


class ManageProjectUsersView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUserForm
    template_name = "projects/manage_project_users.html"
    context_object_name = 'project'
    permission_required = "auth.change_user"

    def has_permission(self):
        project = self.get_object()
        return super().has_permission() and project.users.filter(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('webapp:detailed_project_view', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        return context

from django.contrib import admin

from webapp.models import Task, Status, Type, Project


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'summary']
    list_filter = ['status']
    search_fields = ['summary', 'description']
    fields = ['summary', 'description', 'status', 'type']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    fields = ['name']


admin.site.register(Status, StatusAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    fields = ['name']


admin.site.register(Type, TypeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_date', 'end_date', 'name', 'description']
    list_display_links = ['id', 'name']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name', 'description']
    fields = ['start_date', 'end_date', 'name', 'description', 'users']


admin.site.register(Project, ProjectAdmin)

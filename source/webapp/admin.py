from django.contrib import admin

from webapp.models import Task, Status, Type


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    list_display_links = ['id', 'summary']
    list_filter = ['status', 'type']
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

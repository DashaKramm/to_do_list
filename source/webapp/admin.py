from django.contrib import admin

from webapp.models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'status', 'date_of_completion']
    list_display_links = ['id', 'description']
    list_filter = ['status']
    search_fields = ['description']
    fields = ['description', 'status', 'date_of_completion']


admin.site.register(Task, TaskAdmin)

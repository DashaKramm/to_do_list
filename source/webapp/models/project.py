from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    name = models.CharField(max_length=80, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    users = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name="Пользователи")

    def get_absolute_url(self):
        return reverse('webapp:detailed_project_view', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

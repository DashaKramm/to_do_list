from django.db import models

# Create your models here.
status_choices = [('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]


class Task(models.Model):
    description = models.CharField(max_length=50, null=False, blank=False, verbose_name="Описание")
    status = models.CharField(max_length=30, null=False, blank=False, verbose_name="Статус", default="new",
                              choices=status_choices)
    date_of_completion = models.DateField(null=True, blank=True, verbose_name="Дата выполнения", default=None)
    detailed_description = models.TextField(null=True, blank=True, verbose_name="Подробное описание")

    def __str__(self):
        return f"{self.pk}) {self.description} ({self.status})"

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

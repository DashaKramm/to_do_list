from django.db import models


# Create your models here.
class Task(models.Model):
    summary = models.CharField(max_length=80, verbose_name="Краткое описание")
    description = models.TextField(null=True, blank=True, verbose_name="Полное описание")
    status = models.ForeignKey('webapp.Status', related_name='status_tasks', on_delete=models.PROTECT,
                               verbose_name="Статус")
    type = models.ManyToManyField('webapp.Type', related_name='type_tasks', verbose_name="Тип")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self):
        return f"{self.summary} ({self.status.name})"

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

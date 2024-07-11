from django.db import models


# Create your models here.
class Task(models.Model):
    summary = models.CharField(max_length=80, verbose_name="Краткое описание")
    description = models.TextField(null=True, blank=True, verbose_name="Полное описание")
    status = models.ForeignKey('webapp.Status', related_name='status_tasks', on_delete=models.CASCADE,
                               verbose_name="Статус")
    type = models.ForeignKey('webapp.Type', related_name='type_tasks', on_delete=models.CASCADE,
                             verbose_name="Тип")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self):
        return f"{self.summary} ({self.status.name})"

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

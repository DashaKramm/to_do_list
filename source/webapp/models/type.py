from django.db import models


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

# Generated by Django 5.0.6 on 2024-07-11 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='summary',
            field=models.CharField(max_length=80, verbose_name='Краткое описание'),
        ),
    ]

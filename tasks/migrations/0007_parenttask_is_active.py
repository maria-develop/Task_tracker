# Generated by Django 5.1.5 on 2025-01-26 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_employee_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parenttask',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Признак активности задачи'),
        ),
    ]

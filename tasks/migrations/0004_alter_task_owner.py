# Generated by Django 5.1.5 on 2025-01-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.IntegerField(blank=True, null=True, verbose_name='создатель'),
        ),
    ]

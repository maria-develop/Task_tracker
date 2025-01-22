from django.db import models

from config import settings
from users.models import Employee, Manager, User
from .validators import validate_manager_can_create_task, validate_manager_cannot_assign_to_self


NULLABLE = {"null": True, "blank": True}


class ParentTask(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название главной задачи")
    start_date = models.DateField(verbose_name="Дата начала")
    planned_end_date = models.DateField(verbose_name="Плановый срок выполнения")
    end_date = models.DateField(**NULLABLE, verbose_name="Дата окончания")
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        verbose_name="Менеджер",
        related_name="parent_tasks"
    )
    description = models.TextField(verbose_name="Описание задачи", **NULLABLE)

    def __str__(self):
        return f"{self.title}, {self.manager}"

    class Meta:
        verbose_name = "Главная задача"
        verbose_name_plural = "Главные задачи"


class Task(models.Model):
    STATUS_DONE = "done"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_NOT_STARTED = "not_started"
    STATUS = [
        (STATUS_DONE, "Выполнено"),
        (STATUS_IN_PROGRESS, "В процессе выполнения"),
        (STATUS_NOT_STARTED, "Не приступал к выполнению"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    parent_task = models.ForeignKey(
        ParentTask, on_delete=models.CASCADE, **NULLABLE, verbose_name="Главная задача", related_name="sub_tasks"
    )

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Иcполнитель", related_name="tasks"
    )
    limit_time = models.CharField(max_length=20, verbose_name="Срок выполнения задачи")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(
        max_length=20, choices=STATUS, default=STATUS_NOT_STARTED, verbose_name="Статус"
    )
    comments = models.TextField(verbose_name="Комментарии к задаче", **NULLABLE)
    owner = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        verbose_name="Создатель задачи",
        related_name="created_tasks",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Признак активности задачи"
    )
    is_important = models.BooleanField(
        default=False, verbose_name="Признак важности задачи"
    )

    def clean(self):
        """Общая валидация для модели."""
        validate_manager_can_create_task(self.owner)
        validate_manager_cannot_assign_to_self(self.owner, self.employee)

    def mark_as_done(self, user):
        """Завершить задачу."""
        from .validators import validate_mark_as_done

        validate_mark_as_done(user, self.status)
        self.status = self.STATUS_DONE
        self.save()

    def __str__(self):
        return f"{self.title}: {self.status}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

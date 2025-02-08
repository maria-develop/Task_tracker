from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .validators import validate_mark_as_done


NULLABLE = {"null": True, "blank": True}


class Manager(AbstractBaseUser, PermissionsMixin):
    """Модель менеджера.

        Обязвтельные поля:
            email (EmailField): Уникальный email для входа в систему.
            full_name (str): ФИО менеджера.
            position (str): Должность.
            department (str): Структурное подразделение.
            vacation_status (bool): Статус отсутствия на рабочем месте.
            is_active (bool): Активен ли аккаунт.
            is_staff (bool): Является ли сотрудником.

        Methods:
            __str__: Возвращает строковое представление в формате "ФИО (подразделение)".
        """
    email = models.EmailField(unique=True, verbose_name="Почта")
    username = None
    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО",
        help_text="Иванов И.И.",
    )
    position = models.CharField(max_length=100, verbose_name="Должность")
    department = models.CharField(max_length=100, blank=True, verbose_name="Структурное подразделение")
    vacation_status = models.BooleanField(
        default=False,
        verbose_name="Статус отсутствия на рабочем месте",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="manager_set",  # Уникальное related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="manager_user_permissions",  # Уникальное related_name
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.department})"

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"


class Employee(models.Model):
    """Модель сотрудника-исполнителя задач.

        Атрибуты:
            email (EmailField): Уникальный email сотрудника.
            full_name (str): ФИО сотрудника.
            department (str): Отдел/тип занятости (самозанятый, ИП и т.д.).
            manager (ForeignKey): Связанный менеджер.
            is_active (bool): Активен ли сотрудник.
        """
    email = models.EmailField(unique=True, verbose_name="Почта")
    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО",
        help_text="Иванов И.И.",
        **NULLABLE,
    )
    department = models.CharField(
        max_length=100,
        verbose_name="Структурное подразделение",
        help_text="отдел, гпх, самозанятый, ИП, юр.лицо",
        **NULLABLE,)
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE,)
    vacation_status = models.BooleanField(
        default=False,
        verbose_name="Статус отсутствия на рабочем месте",
        **NULLABLE,
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    manager = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        related_name="employees",
        verbose_name="Менеджер",
        **NULLABLE,
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="employee_set",  # Уникальное related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="employee_user_permissions",  # Уникальное related_name
        blank=True,
    )

    def __str__(self):
        return f"{self.full_name} ({self.department})"

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"


class ParentTask(models.Model):
    """Родительская задача, объединяющая подзадачи.

        Обязательные поля:
            title (str): Название задачи.
            start_date (date): Дата начала.
            planned_end_date (date): Плановый срок выполнения.
            is_active (bool): Активна ли задача.
        Атрибуты не обязательны к заполнению:
            end_date (date): Фактическая дата завершения.
            manager (ForeignKey): Ответственный менеджер.
            description (str): Описание задачи.
            status (str): Статус выполнения (done/in_progress/not_started).

        """
    STATUS_DONE = "done"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_NOT_STARTED = "not_started"
    STATUS = [
        (STATUS_DONE, "Выполнено"),
        (STATUS_IN_PROGRESS, "В процессе выполнения"),
        (STATUS_NOT_STARTED, "Не приступал к выполнению"),
    ]
    title = models.CharField(max_length=255, verbose_name="Название главной задачи")
    start_date = models.DateField(verbose_name="Дата начала")
    planned_end_date = models.DateField(verbose_name="Плановый срок выполнения")
    end_date = models.DateField(**NULLABLE, verbose_name="Дата окончания")
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        verbose_name="Менеджер",
        related_name="parent_tasks",
        **NULLABLE,
    )
    description = models.TextField(verbose_name="Описание задачи", **NULLABLE)
    status = models.CharField(
        max_length=20, choices=STATUS, default=STATUS_NOT_STARTED, verbose_name="Статус", **NULLABLE
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Признак активности задачи"
    )

    def __str__(self):
        return f"{self.title}, {self.manager}"

    class Meta:
        ordering = ["-start_date"]  # Сортировка по убыванию даты начала
        verbose_name = "Главная задача"
        verbose_name_plural = "Главные задачи"


class Task(models.Model):
    """Задача, назначенная исполнителю.

        Атрибуты:
            title (str): Название задачи.
            parent_task (ForeignKey): Родительская задача.
            employee (ForeignKey): Исполнитель.
            limit_time (str): Срок выполнения в днях.
            start_date (date): Дата начала.
            end_date (date): Фактическая дата завершения.
            status (str): Статус выполнения.
            comments (str): Описание задачи.
            is_active (bool): Признак активности задачи.
            is_important (bool): Признак важности задачи.
        """
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
        ParentTask,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Главная задача",
        related_name="tasks"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Иcполнитель",
        related_name="tasks"
    )
    limit_time = models.CharField(max_length=20, verbose_name="Срок выполнения задачи")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания", **NULLABLE)
    status = models.CharField(
        max_length=20, choices=STATUS, default=STATUS_NOT_STARTED, verbose_name="Статус"
    )
    comments = models.TextField(verbose_name="Комментарии к задаче", **NULLABLE)
    is_active = models.BooleanField(
        default=True, verbose_name="Признак активности задачи"
    )
    is_important = models.BooleanField(
        default=False, verbose_name="Признак важности задачи"
    )

    def mark_as_done(self, user):
        """Завершить задачу."""
        validate_mark_as_done(user, self.status)
        self.status = self.STATUS_DONE
        self.save()

    def __str__(self):
        return f"{self.title}: {self.status}"

    class Meta:
        ordering = ["-start_date"]  # Сортировка по убыванию даты начала
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

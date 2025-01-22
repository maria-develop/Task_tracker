from django.contrib.auth.models import AbstractBaseUser, Group, Permission, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта")
    username = models.CharField(
        max_length=100,
        verbose_name="Имя",
        help_text="Иванов И.И.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.email


class User(BaseUser):
    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"


class Manager(BaseUser):
    department = models.CharField(max_length=100, blank=True, verbose_name="Отдел")

    groups = models.ManyToManyField(
        Group,
        related_name="manager_groups",  # Уникальное имя
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="manager_permissions",  # Уникальное имя
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.department})"

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"


class Employee(BaseUser):
    phone = models.CharField(max_length=35, blank=True, verbose_name="Телефон")
    manager = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True,
        verbose_name="Менеджер",
    )
    groups = models.ManyToManyField(
        Group,
        related_name="employee_groups",  # Уникальное имя
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="employee_permissions",  # Уникальное имя
        blank=True
    )

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

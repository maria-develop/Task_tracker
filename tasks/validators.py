import re
from rest_framework.serializers import ValidationError


def validate_manager_can_create_task(owner):
    """Проверка: только менеджер может создавать задачи."""
    if not getattr(owner, "is_manager", False):
        raise ValidationError("Только менеджер может создавать задачи.")


def validate_manager_cannot_assign_to_self(owner, employee):
    """Проверка: менеджер не может назначить задачу самому себе."""
    if owner == employee:
        raise ValidationError("Менеджер не может назначить задачу самому себе.")


def validate_mark_as_done(user, status):
    """Проверка: только менеджер может завершить задачу, если она в процессе выполнения."""
    if not getattr(user, "is_manager", False):
        raise ValidationError("Только менеджер может завершить задачу.")
    if status != "in_progress":
        raise ValidationError("Задачу можно завершить только если она в процессе выполнения.")


class TitleValidator:
    """Проверка: поле title должно содержать только разрешенные символы."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"^[а-яА-Яa-zA-Z0-9\.\-\,\№\s]+$")
        if not reg.match(value):
            raise ValidationError(
                f"{self.field} может содержать только буквы, цифры, точки, дефисы, запятые и пробелы."
            )

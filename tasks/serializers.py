from rest_framework.serializers import ModelSerializer, SerializerMethodField, UniqueTogetherValidator, CharField
from django.db.models import Q

from .models import Task, ParentTask, Manager, Employee
from .validators import TitleValidator


class ManagerSerializer(ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Обязательно хэширование
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Хэшируем пароль при обновлении
        instance.save()
        return instance

    class Meta:
        model = Manager
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Скрыть пароль в выводе
        }


class ManagerActiveTasksSerializer(ModelSerializer):
    summ_active_tasks = SerializerMethodField()
    tasks = SerializerMethodField()

    def get_summ_active_tasks(self, manager):
        return ParentTask.objects.filter(Q(manager=manager.id), Q(is_active=True)).count()

    def get_tasks(self, manager):
        tasks = ParentTask.objects.filter(manager=manager.id)
        tasks_list = []
        for task in tasks:
            if task.is_active:
                tasks_list.append(task.title)
        return tasks_list

    class Meta:
        model = Manager
        fields = ("full_name", "tasks", "summ_active_tasks")


class EmployeeSerializer(ModelSerializer):

    def create(self, validated_data):
        """Создание пользователя с захэшированным паролем"""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Хэшируем пароль при обновлении
        instance.save()
        return instance

    class Meta:
        model = Employee
        fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True},  # Скрыть пароль в выводе
        # }


class TaskWithParentSerializer(ModelSerializer):
    parent_task = CharField(source="parent_task.title", read_only=True)

    class Meta:
        model = Task
        fields = ["title", "parent_task"]


class EmployeeActiveTasksSerializer(ModelSerializer):
    summ_active_tasks = SerializerMethodField()
    tasks = SerializerMethodField()  # Для кастомной логики отображения задач

    def get_summ_active_tasks(self, employee):
        # Подсчитываем количество активных задач напрямую
        return Task.objects.filter(employee=employee, is_active=True).count()

    def get_tasks(self, employee):
        # Выбираем только активные задачи и возвращаем список с их названиями и родительскими задачами
        active_tasks = Task.objects.filter(employee=employee, is_active=True)
        return [
            {
                "title": task.title,
                "parent_task": task.parent_task.title if task.parent_task else None,
            }
            for task in active_tasks
        ]

    class Meta:
        model = Employee
        fields = ("full_name", "tasks", "summ_active_tasks")


class ParentTaskSerializer(ModelSerializer):
    completion_days = SerializerMethodField()
    title = CharField(
        validators=[TitleValidator(field="title")],
    )

    def get_completion_days(self, task):
        if task.end_date and task.start_date:
            return (task.end_date - task.start_date).days

    class Meta:
        model = ParentTask
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(fields=["title"], queryset=ParentTask.objects.all()),
        ]


class TaskSerializer(ModelSerializer):
    completion_days = SerializerMethodField()
    title = CharField(
        validators=[TitleValidator(field="title")],
    )

    def get_completion_days(self, task):
        if task.end_date and task.start_date:
            return (task.end_date - task.start_date).days

    class Meta:
        model = Task
        fields = '__all__'


class BaseTaskSerializer(ModelSerializer):
    """Базовый класс"""
    completion_days = SerializerMethodField()
    available_people = SerializerMethodField()

    def get_completion_days(self, task):
        if task.end_date and task.start_date:
            return (task.end_date - task.start_date).days
        return None

    def get_available_people(self, task, queryset, person_field):
        """
        Определяет доступных сотрудников или менеджеров.
        :param task: текущая задача
        :param queryset: QuerySet сотрудников или менеджеров
        :param person_field: поле, связанное с задачей (например, 'employee' или 'manager')
        :return: список имён доступных сотрудников или менеджеров
        """
        people_data = {}
        # available_people = []

        # Подсчитать количество задач для каждого человека
        for person in queryset:
            people_data[person.pk] = person.task_set.count()

        # Найти наименее загруженного
        min_count = min(people_data.values(), default=0)

        # Добавить в список доступных
        available_people = [
            person.full_name for person in queryset if people_data[person.pk] == min_count
        ]

        # Проверить задачи с той же родительской задачей
        for person in queryset:
            tasks = person.task_set.filter(parent_task=task.parent_task)
            if (
                len(tasks) - min_count <= 2
                and person.full_name not in available_people
            ):
                available_people.append(person.full_name)

        return available_people


class ImportantTaskSerializer(BaseTaskSerializer):
    current_employees = SerializerMethodField()
    parent_task_title = SerializerMethodField()

    def get_current_employees(self, task):
        """Получаем текущих сотрудников для задачи"""
        return [task.employee.full_name] if task.employee else []

    def get_parent_task_title(self, task):
        """Проверяем связь с ParentTask"""
        return task.parent_task.title if task.parent_task else None

    def get_available_people(self, task):
        return super().get_available_people(task, Employee.objects.all(), "employee")

    class Meta:
        model = Task
        fields = (
            "title",
            "parent_task_title",
            "start_date",
            "end_date",
            "completion_days",
            "current_employees",
            "available_people",
            "is_important",
        )

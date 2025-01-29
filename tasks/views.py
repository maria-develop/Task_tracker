from django.db.models import Q, Count
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from rest_framework.filters import SearchFilter

from .models import Task, ParentTask, Manager, Employee
from .paginations import ParentTaskPageNumberPagination, TaskPageNumberPagination
from .serializers import ParentTaskSerializer, TaskSerializer, ManagerSerializer, EmployeeSerializer, \
    ManagerActiveTasksSerializer, EmployeeActiveTasksSerializer, ImportantTaskSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")  # Вывод email и пароля
        return super().post(request, *args, **kwargs)


class ManagerListAPIView(ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerRetrieveAPIView(RetrieveAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerActiveTasksSerializer


class ManagerCreateAPIView(CreateAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class ManagerDestroyAPIView(DestroyAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class ManagerUpdateAPIView(UpdateAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class ManagerActiveTasksListAPIView(ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerActiveTasksSerializer
    filter_backends = [SearchFilter]
    search_fields = ["full_name"]

    def get_queryset(self):
        self.queryset = (
            Manager.objects.annotate(tasks_count=Count("parent_tasks"))
            # .select_related("profile")  # Оптимизация связи с профилем
            .prefetch_related("parent_tasks")  # Предзагрузка связанных задач
            .order_by("-tasks_count")
        )
        return self.queryset


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveTasksSerializer


class EmployeeCreateAPIView(CreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeDestroyAPIView(DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeUpdateAPIView(UpdateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class BusyEmployeesListAPIView(ListAPIView):
    queryset = Employee.objects.prefetch_related("tasks")  # Загружаем связанные задачи
    serializer_class = EmployeeActiveTasksSerializer


class ParentTaskCreateAPIView(CreateAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        task.owner = self.request.user
        task.save()


class ParentTaskListAPIView(ListAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer
    pagination_class = ParentTaskPageNumberPagination


class ParentTaskRetrieveAPIView(RetrieveAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer


class ParentTaskUpdateAPIView(UpdateAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer


class ParentTaskDestroyAPIView(DestroyAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        task.owner = self.request.user
        task.save()


class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPageNumberPagination


class TaskRetrieveAPIView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ImportantTaskListAPIView(ListAPIView):
    serializer_class = ImportantTaskSerializer

    def get(self, request, *args, **kwargs):
        active_task_limit = 2  # Максимальное количество активных задач

        important_tasks = Task.objects.filter(
            is_important=True, status=Task.STATUS_NOT_STARTED
        ).select_related("parent_task")

        employees = Employee.objects.annotate(
            active_task_count=Count('tasks', filter=Q(tasks__status=Task.STATUS_IN_PROGRESS))
        ).exclude(active_task_count__gt=active_task_limit).order_by('active_task_count')

        data = []
        for task in important_tasks:
            suitable_employees = employees.filter(
                Q(tasks__parent_task=task.parent_task) | Q(active_task_count__lte=active_task_limit)
            ).values_list("full_name", flat=True)

            # Используем множество (set) для уникальных имен сотрудников
            unique_suitable_employees = set(suitable_employees)

            data.append({
                "task_name": task.title,
                "parent_task": task.parent_task.title if task.parent_task else None,
                "due_date": task.limit_time,
                "suitable_employees": list(unique_suitable_employees)
            })

        return Response(data)

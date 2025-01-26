from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from tasks.apps import TasksConfig
from tasks.views import (
    ManagerCreateAPIView, ManagerListAPIView, ManagerRetrieveAPIView, ManagerUpdateAPIView, ManagerDestroyAPIView,
    EmployeeCreateAPIView, EmployeeListAPIView, EmployeeRetrieveAPIView, EmployeeUpdateAPIView, EmployeeDestroyAPIView,
    ParentTaskCreateAPIView, ParentTaskDestroyAPIView, ParentTaskListAPIView, ParentTaskRetrieveAPIView,
    ParentTaskUpdateAPIView,
    TaskCreateAPIView, TaskDestroyAPIView, TaskListAPIView, TaskRetrieveAPIView, TaskUpdateAPIView,
    CustomTokenObtainPairView, BusyEmployeesListAPIView, ManagerActiveTasksListAPIView,
    ImportantTaskListAPIView,
)

app_name = TasksConfig.name

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("m/", ManagerListAPIView.as_view(), name="managers_list"),
    path("m/<int:pk>/", ManagerRetrieveAPIView.as_view(), name="manager_retrieve"),
    path("m/create/", ManagerCreateAPIView.as_view(), name="manager_create"),
    path("m/<int:pk>/update/", ManagerUpdateAPIView.as_view(), name="manager_update"),
    path("m/<int:pk>/delete/", ManagerDestroyAPIView.as_view(), name="manager_delete"),
    path("m/active_tasks/", ManagerActiveTasksListAPIView.as_view(), name="manager_active_tasks_list"),

    path("emp/", EmployeeListAPIView.as_view(), name="employees_list"),
    path("emp/<int:pk>/", EmployeeRetrieveAPIView.as_view(), name="employee_retrieve"),
    path("emp/create/", EmployeeCreateAPIView.as_view(), name="employee_create"),
    path("emp/<int:pk>/update/", EmployeeUpdateAPIView.as_view(), name="employee_update"),
    path("emp/<int:pk>/delete/", EmployeeDestroyAPIView.as_view(), name="employee_delete"),
    path("emp/busy_tasks/", BusyEmployeesListAPIView.as_view(), name="employee_busy_tasks_list"),  # занятые сотрудники

    path("", ParentTaskListAPIView.as_view(), name="parent_task_list"),
    path("<int:pk>/", ParentTaskRetrieveAPIView.as_view(), name="parent_task_retrieve"),
    path("create/", ParentTaskCreateAPIView.as_view(), name="parent_task_create"),
    path("<int:pk>/update/", ParentTaskUpdateAPIView.as_view(), name="parent_task_update"),
    path("<int:pk>/delete/", ParentTaskDestroyAPIView.as_view(), name="parent_task_delete"),

    path("t/", TaskListAPIView.as_view(), name="task_list"),
    path("t/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task_retrieve"),
    path("t/create/", TaskCreateAPIView.as_view(), name="task_create"),
    path("t/<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task_update"),
    path("t/<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task_delete"),
    path("t/important/", ImportantTaskListAPIView.as_view(), name="important_task_list"),  # важные задачи
]

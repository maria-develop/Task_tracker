from django.urls import path

from .apps import TasksConfig
from .views import (ParentTaskCreateAPIView, ParentTaskDestroyAPIView, ParentTaskListAPIView,
                    ParentTaskRetrieveAPIView, ParentTaskUpdateAPIView,
                    TaskCreateAPIView, TaskDestroyAPIView, TaskListAPIView,
                    TaskRetrieveAPIView, TaskUpdateAPIView,
                    )

app_name = TasksConfig.name


urlpatterns = [
    path("list/", ParentTaskListAPIView.as_view(), name="parent_task_list"),
    path("<int:pk>/", ParentTaskRetrieveAPIView.as_view(), name="parent_task_retrieve"),
    path("create/", ParentTaskCreateAPIView.as_view(), name="parent_task_create"),
    path("<int:pk>/delete/", ParentTaskDestroyAPIView.as_view(), name="parent_task_delete"),
    path("<int:pk>/update/", ParentTaskUpdateAPIView.as_view(), name="parent_task_update"),
    path("task/list/", TaskListAPIView.as_view(), name="task_list"),
    path("task/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task_retrieve"),
    path("task/create/", TaskCreateAPIView.as_view(), name="task_create"),
    path("task/<int:pk>/delete/", TaskDestroyAPIView.as_view(), name="task_delete"),
    path("task/<int:pk>/update/", TaskUpdateAPIView.as_view(), name="task_update"),
]

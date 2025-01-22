from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from users.permissions import IsOwner, IsManagerOrAdmin

from .models import Task, ParentTask
from .paginations import ParentTaskPageNumberPagination, TaskPageNumberPagination
from .serializers import ParentTaskSerializer, TaskSerializer


class ParentTaskCreateAPIView(CreateAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    # def perform_create(self, serializer):
    #     task = serializer.save()
    #     task.owner = self.request.user
    #     task.save()


class ParentTaskListAPIView(ListAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer
    pagination_class = ParentTaskPageNumberPagination
    permission_classes = [IsManagerOrAdmin]

    # def get_queryset(self):
    #     queryset = self.queryset.filter(manager=self.request.user)
    #     return queryset


class ParentTaskRetrieveAPIView(RetrieveAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer
    permission_classes = (IsOwner,)


class ParentTaskUpdateAPIView(UpdateAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer
    permission_classes = (IsOwner,)


class ParentTaskDestroyAPIView(DestroyAPIView):
    queryset = ParentTask.objects.all()
    serializer_class = ParentTaskSerializer
    permission_classes = (IsOwner,)


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    # def perform_create(self, serializer):
    #     task = serializer.save()
    #     task.owner = self.request.user
    #     task.save()


class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = TaskPageNumberPagination

    # def get_queryset(self):
    #     queryset = self.queryset.filter(manager=self.request.user)
    #     return queryset


class TaskRetrieveAPIView(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwner,)


class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwner,)


class TaskDestroyAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsOwner,)

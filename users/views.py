from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import User, Manager, Employee
from users.serializers import UserSerializer, ManagerSerializer, EmployeeSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class ManagerListAPIView(ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerRetrieveAPIView(RetrieveAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerCreateAPIView(CreateAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()

    def perform_create(self, serializer):
        manager = serializer.save(is_active=True)
        manager.set_password(Manager.password)
        manager.save()


class ManagerDestroyAPIView(DestroyAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class ManagerUpdateAPIView(UpdateAPIView):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateAPIView(CreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def perform_create(self, serializer):
        employee = serializer.save(is_active=True)
        employee.set_password(Employee.password)
        employee.save()


class EmployeeDestroyAPIView(DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeUpdateAPIView(UpdateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

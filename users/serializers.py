from rest_framework.serializers import ModelSerializer

from users.models import User, Manager, Employee


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ManagerSerializer(ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

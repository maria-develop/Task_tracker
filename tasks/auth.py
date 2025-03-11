from django.contrib.auth.backends import ModelBackend
from users.models import User
from tasks.models import Manager


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Попробуем сначала найти пользователя в модели User
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass

        # Если не нашли в User, пробуем в Manager
        try:
            manager = Manager.objects.get(email=email)
            if manager.check_password(password) and self.user_can_authenticate(manager):
                return manager
        except Manager.DoesNotExist:
            pass

        # try:
        #     employee = Employee.objects.get(email=email)
        #     if employee.check_password(password) and self.user_can_authenticate(employee):
        #         return employee
        # except Employee.DoesNotExist:
        #     pass

        return None

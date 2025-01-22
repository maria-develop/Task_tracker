from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserViewSet
from users.views import (
    ManagerCreateAPIView,
    ManagerListAPIView,
    ManagerRetrieveAPIView,
    ManagerUpdateAPIView,
    ManagerDestroyAPIView,
    EmployeeCreateAPIView,
    EmployeeListAPIView,
    EmployeeRetrieveAPIView,
    EmployeeUpdateAPIView,
    EmployeeDestroyAPIView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", ManagerCreateAPIView.as_view(), name="register"),
    path("", ManagerListAPIView.as_view(), name="managers_list"),
    path("<int:pk>/", ManagerRetrieveAPIView.as_view(), name="manager_retrieve"),
    path("create/", ManagerCreateAPIView.as_view(), name="manager_create"),
    path("<int:pk>/update/", ManagerUpdateAPIView.as_view(), name="manager_update"),
    path("<int:pk>/delete/", ManagerDestroyAPIView.as_view(), name="manager_delete"),
    path("emp/register/", EmployeeCreateAPIView.as_view(), name="emp_register"),
    path("emp/", EmployeeListAPIView.as_view(), name="employees_list"),
    path("emp/<int:pk>/", EmployeeRetrieveAPIView.as_view(), name="employee_retrieve"),
    path("emp/create/", EmployeeCreateAPIView.as_view(), name="employee_create"),
    path("emp/<int:pk>/update/", EmployeeUpdateAPIView.as_view(), name="employee_update"),
    path("emp/<int:pk>/delete/", EmployeeDestroyAPIView.as_view(), name="employee_delete"),
]
urlpatterns += router.urls

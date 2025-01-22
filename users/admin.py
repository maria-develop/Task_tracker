from django.contrib import admin

from users.models import Manager, User, Employee
import logging

logger = logging.getLogger(__name__)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    list_filter = ("id", "email")


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    list_filter = ("id", "username", "email")
    search_fields = ("email", "username", "department")
    ordering = ("email",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    list_filter = ("id", "username", "email")
    search_fields = ("email", "username")
    ordering = ("email",)

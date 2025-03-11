from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import ParentTask, Task, Manager, Employee


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    list_display = ("id", "full_name", "email")
    list_filter = ("id", "full_name", "email")
    search_fields = ("email", "full_name", "department")
    ordering = ("email",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "department")
    list_filter = ("id", "full_name", "email", "department")
    search_fields = ("email", "full_name", "department")
    ordering = ("email",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "employee",
        "parent_task",
        "start_date",
        "end_date",
        "status",
        "comments",
    )
    list_filter = ("employee",)
    search_fields = ("title",)


@admin.register(ParentTask)
class ParentTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "start_date",
        "planned_end_date",
        "end_date",
        "manager",
        "description",
    )
    list_filter = ("title", "manager",)
    search_fields = ("title",)

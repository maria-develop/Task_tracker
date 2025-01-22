from django.contrib import admin

from tasks.models import ParentTask, Task
from users.models import Manager


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
        "owner",
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

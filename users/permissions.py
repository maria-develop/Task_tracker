from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать объект только его владельцам.
    Предполагается, что экземпляр модели имеет атрибут `owner`.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsManagerOrAdmin(IsAuthenticated):
    """Доступ только для менеджеров или администраторов."""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.is_superuser or isinstance(request.user, Manager)
        )

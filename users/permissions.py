from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать объект только его владельцам.
    Предполагается, что экземпляр модели имеет атрибут `owner`.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

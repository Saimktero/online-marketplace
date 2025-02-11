from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
       Разрешает чтение всем (GET), но изменение (POST, PUT, DELETE) только администраторам.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return request.user.is_authenticated and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
        Доступ разрешён только владельцу заказа или админу.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff



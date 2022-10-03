from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка, что пользователь является администратором."""
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.is_admin):
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка, что пользователь авторизован, как админ.
    Иначе доступ только к get запросам.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser)):
            return True
        return False


class IsAuthorIsModeratorIsAdminOrReadOnly(permissions.BasePermission):
    """Проверка, что пользователь - автор/модератор/админ.
    Проверка, что допущены для редактирования данных.
     """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and (
                request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator):
            return True
        return False

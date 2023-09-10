from rest_framework import permissions


class IsAdminReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только для чтения любому пользователю,
    но разрешает изменение или удаление только
    пользователям-администраторам.
    """

    def has_permission(self, request, view):
        """
        Проверяет, если метод безопасный то доступ разрешен,
        если пользователь аутентифицирован и является администратором,
        то доступ разрешен.
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа для автора либо администратора."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_staff
                or obj.author == request.user)


class IsAuthorOrReadOnlyOrAnonymous(permissions.BasePermission):
    """
    Разрешает доступ только авторам, а также анонимным пользователям на чтение.
    """

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated):
            return True
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Разрешает доступ только авторизованным пользователям.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

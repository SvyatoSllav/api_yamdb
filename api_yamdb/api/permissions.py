from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать объект только
    администраторам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_staff)


class AuthorModerAdmin(permissions.BasePermission):
    """
    добавлять авторизизированным, а редактировать и удалять объект авторам,
    Пользовательское разрешение, позволяющее просматривать всем,
    модераторам и админам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author == request.user or request.user.is_staff)
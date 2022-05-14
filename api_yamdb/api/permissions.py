from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать объект только
    администраторам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_superuser)))


class AuthorModerAdmin(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее просматривать всем,
    добавлять авторизизированным, а редактировать и удалять
    объект авторам, модераторам и админам

    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.is_superuser)

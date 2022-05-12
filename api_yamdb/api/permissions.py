from rest_framework import permissions


class AuthorModerAdmin(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее просматривать всем,
    добавлять авторизизированным, а редактировать и удалять объект авторам,
    модераторам и админам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff

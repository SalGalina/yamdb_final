from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение автору изменять или удалять свой объект.
    """

    def has_object_permission(self, request, view, obj):
        return ((request.user
                 and request.user.is_authenticated
                 and obj.author == request.user)
                or request.method in permissions.SAFE_METHODS
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение админам изменять или удалять объекты.
    Остальным только на чтение.
    """

    def has_object_permission(self, request, view, obj):
        return ((request.user
                 and request.user.is_authenticated
                 and request.user.is_staff
                 and request.user.role == User.ADMIN)
                or request.method in permissions.SAFE_METHODS
                )

    def has_permission(self, request, view):
        return ((request.user
                 and request.user.is_authenticated
                 and request.user.is_staff
                 and request.user.role == User.ADMIN)
                or request.method in permissions.SAFE_METHODS
                )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_authenticated)
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.user
             and request.user.is_authenticated
             and obj.author == request.user
             )
            or (request.user
                and request.user.is_authenticated
                and request.user.is_staff
                and request.user.role == User.ADMIN
                )
            or (request.user
                and request.user.is_authenticated
                and request.user.role == User.MODERATOR
                )
            or request.method in permissions.SAFE_METHODS
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.role == User.ADMIN
        )

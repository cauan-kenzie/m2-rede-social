from rest_framework import permissions, views


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request: views.Request, _):
        SAFE_METHODS = ("POST",)

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated

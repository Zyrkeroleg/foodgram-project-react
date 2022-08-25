from rest_framework import permissions



class IsAuthorPermission(permissions.BasePermission):
    """ Права доступа только для автора """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
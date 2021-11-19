from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        else:
            return False

class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        else:
            return False


class IsUserAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name__in=['administrador', 'funcionario']).exists():
            return True
        return False
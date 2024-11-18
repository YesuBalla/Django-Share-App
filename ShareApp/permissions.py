from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    """
    Allows access only to Ops Users or superusers.
    """

    def has_permission(self, request, view):
        # Allow access if the user is a superuser or belongs to the 'Ops' group
        if request.user.groups.filter(name='Ops').exists():
            return True
        return False


class IsClientUser(BasePermission):
    """
    Allows access only to Client Users or superusers.
    """

    def has_permission(self, request, view):
        # Allow access if the user is a superuser or belongs to the 'Client' group
        if request.user.groups.filter(name='Client').exists():
            return True
        return False

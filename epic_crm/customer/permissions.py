from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAssignedOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or request.user == obj.affected_user:
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')

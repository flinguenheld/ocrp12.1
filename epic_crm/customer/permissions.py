from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAssignedOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.user.is_staff or
            request.user == obj.assigned_user):
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')


class CanAddCustomerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if (request.user.is_staff or
            'customer.add_customer' in request.user.get_all_permissions()):
            return True

        raise PermissionDenied('Only salespeople or staff are authorized.')

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAssignedOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if (request.user.is_staff or
            request.user.customer_of.filter(pk=request.data['customer'])):
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')


class IsAssignedOrStaffObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.user.is_staff or
            request.user.customer_of.filter(contract_of=obj)):
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')

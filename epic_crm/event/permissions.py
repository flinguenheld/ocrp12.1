from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAssignedToThisCustomerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if (request.user.is_staff or
            request.user.customer_of.filter(contract_of__pk=request.data['contract'])):
            return True

        raise PermissionDenied('Only the customer assigned user or staff are authorized.')


class IsAssignedToThisEventOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.user.is_staff or
            request.user.event_of.filter(pk=obj.pk)):
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')

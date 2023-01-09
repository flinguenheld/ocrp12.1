from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from epic_crm.customer.models import Customer


class IsAssignedOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if (request.user.is_staff or
            request.user == get_object_or_404(Customer, pk=request.data['customer']).assigned_user):
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')


class IsAssignedOrStaffObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or request.user == obj.customer.assigned_user:
            return True

        raise PermissionDenied('Only the assigned user or staff are authorized.')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.contrib.auth.models import Group, Permission
from django.db import connection


# Groups auto-added after the first migration
def init_groups():

    if 'auth_group' in connection.introspection.table_names():

        if not Group.objects.filter(name='sales'):

            group_sales = Group.objects.create(name='sales')
            group_sales.permissions.add(Permission.objects.get(name='Can add customer'))

        if not Group.objects.filter(name='manager'):

            group_manager = Group.objects.create(name='manager')
            group_manager.permissions.add(Permission.objects.get(name='Can view user'))
            group_manager.permissions.add(Permission.objects.get(name='Can add user'))
            group_manager.permissions.add(Permission.objects.get(name='Can change user'))
            group_manager.permissions.add(Permission.objects.get(name='Can delete user'))

            group_manager.permissions.add(Permission.objects.get(name='Can view customer'))
            group_manager.permissions.add(Permission.objects.get(name='Can add customer'))
            group_manager.permissions.add(Permission.objects.get(name='Can change customer'))
            group_manager.permissions.add(Permission.objects.get(name='Can delete customer'))

            group_manager.permissions.add(Permission.objects.get(name='Can view contract'))
            group_manager.permissions.add(Permission.objects.get(name='Can add contract'))
            group_manager.permissions.add(Permission.objects.get(name='Can change contract'))
            group_manager.permissions.add(Permission.objects.get(name='Can delete contract'))

            group_manager.permissions.add(Permission.objects.get(name='Can view event'))
            group_manager.permissions.add(Permission.objects.get(name='Can add event'))
            group_manager.permissions.add(Permission.objects.get(name='Can change event'))
            group_manager.permissions.add(Permission.objects.get(name='Can delete event'))


# --
# Adminsite adapted to superuser and staff
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_filter = ('is_staff', 'is_superuser')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        return User.objects.exclude(is_superuser=True)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj and not request.user.is_superuser:
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['date_joined'].disabled = True
            form.base_fields['last_login'].disabled = True

        return form

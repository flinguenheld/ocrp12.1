from django.contrib.auth.models import Group, Permission
from django.db import connection


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

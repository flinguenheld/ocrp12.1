from django.contrib.auth.models import Group, Permission
from django.db import connection


def init_groups():

    if 'auth_group' in connection.introspection.table_names():

        if not Group.objects.filter(name='sales'):

            group_sales = Group.objects.create(name='sales')
            group_sales.permissions.add(Permission.objects.get(name='Can add customer'))
            # group_sales.permissions.add(Permission.objects.get(name='Can view customer'))

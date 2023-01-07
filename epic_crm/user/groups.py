from django.contrib.auth.models import Group, Permission


def init_groups():

    if not Group.objects.filter(name='sales'):

        group_sales = Group.objects.create(name='sales')
        group_sales.permissions.add(Permission.objects.get(name='Can add customer'))
        # group_sales.permissions.add(Permission.objects.get(name='Can view customer'))

    if not Group.objects.filter(name='tech'):
        group_sales = Group.objects.create(name='tech')
        # group.permissions.add(permission)

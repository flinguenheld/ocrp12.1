from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
# permission = Permission.objects.create(codename='can_publish',
                                       # name='Can Publish Posts',
                                       # content_type=content_type)
# user = User.objects.get(username='duke_nukem')


if not Group.objects.filter(name='sales'):

    group_sales = Group.objects.create(name='sales')
    group_sales.permissions.add(Permission.objects.get(name='Can add customer'))


if not Group.objects.filter(name='tech'):
    group_sales = Group.objects.create(name='tech')
    # group.permissions.add(permission)

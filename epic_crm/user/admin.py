from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .groups import init_groups

# content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
# permission = Permission.objects.create(codename='can_publish',
                                       # name='Can Publish Posts',
                                       # content_type=content_type)
# user = User.objects.get(username='duke_nukem')


# Group initialisation
init_groups()

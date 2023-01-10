from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .groups import init_groups

# Group initialisation
init_groups()


class UserManagerArea(admin.AdminSite):
    site_header = 'User Manager area'
    site_title = 'prout'
    site_index_title = 'aaaaaaprout'


manager_site = UserManagerArea(name='UserManagement')
manager_site.register(Group)
manager_site.register(User)

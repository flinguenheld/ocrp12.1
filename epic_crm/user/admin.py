from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .groups import init_groups


# Groups auto-added after the first migration
init_groups()

# Adminsite adapted to superuser and staff
admin.site.unregister(User)


# --
class AssignmentListFilter(admin.SimpleListFilter):
    title = 'Assignment'
    parameter_name = 'assigned'

    def lookups(self, request, model_admin):
        return (
            ('Tech', 'to an event'),
            ('Sales', 'to a customer'),
         )

    def queryset(self, request, queryset):

        if self.value() == 'Tech':
            return User.objects.exclude(event_of=None)

        if self.value() == 'Sales':
            return User.objects.exclude(customer_of=None)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_filter = ('is_staff', 'groups', AssignmentListFilter)

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

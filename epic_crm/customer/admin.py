from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_filter = ('name', 'email', 'assigned_user', 'date_created')

    list_display = (
            'name',
            'email',
            'assigned_user',
            )

    # def get_exclude(self, request, obj=None):
        # if request.user.is_superuser:
            # return super().get_exclude(request, obj)

        # else:
            # return ['email']

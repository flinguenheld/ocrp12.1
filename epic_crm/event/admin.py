from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_filter = ('name', 'date', 'contract', 'assigned_user')

    list_display = (
            'customer',
            'name',
            'date',
            'assigned_user',
            )

    @admin.display(description="cutomer")
    def customer(self, obj):
        return obj.contract.customer.name

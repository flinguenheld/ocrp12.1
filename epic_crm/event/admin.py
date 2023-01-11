from django.contrib import admin, messages

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_filter = ('name', 'date', 'contract', 'assigned_user')

    list_display = (
            'name',
            'date',
            'customer',
            'assigned_user',
            )

    @admin.display(description="cutomer")
    def customer(self, obj):
        return obj.contract.customer.name

    def save_model(self, request, obj, form, change):
        if not obj.contract.is_signed:
            messages.add_message(request,
                                 messages.WARNING,
                                 f"""The contract '{obj.contract.pk}' used with the new event '{obj.name}'
                                 has not been signed yet""")

        super().save_model(request, obj, form, change)

from django.contrib import admin, messages

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):

    list_filter = ('customer', 'amount', 'date_created', 'date_signed')

    list_display = (
            'date_created',
            'is_signed',
            'customer',
            )

    def save_model(self, request, obj, form, change):
        if obj.amount < 0:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'You have set a negative amount : {obj.amount}')

        super().save_model(request, obj, form, change)

from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):

    list_filter = ('customer', 'amount', 'date_created', 'date_signed')

    list_display = (
            'customer',
            'date_created',
            'date_signed',
            )

from django.contrib import admin, messages

from .models import Contract


class SignedListFilter(admin.SimpleListFilter):
    title = 'Signed'
    parameter_name = 'signed'

    def lookups(self, request, model_admin):
        return (
            ('Signed', 'Signed'),
            ('Unsigned', 'Unsigned'),
         )

    def queryset(self, request, queryset):
        if self.value() == 'Signed':
            return Contract.objects.exclude(date_signed=None)

        if self.value() == 'Unsigned':
            return Contract.objects.filter(date_signed=None)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):

    list_filter = ('customer', 'amount', 'date_created', 'date_signed', SignedListFilter)

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

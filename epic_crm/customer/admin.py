from django.contrib import admin

from .models import Customer


class NewCustomerListFilter(admin.SimpleListFilter):
    title = 'New customer'
    parameter_name = 'new'

    def lookups(self, request, model_admin):
        return (
            ('New', 'New customers'),
            ('Current', 'Already signed once'),
         )

    def queryset(self, request, queryset):
        if self.value() == 'New':
            return Customer.objects.filter(contract_of__date_signed=None)

        if self.value() == 'Current':
            return Customer.objects.exclude(contract_of__date_signed=None)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_filter = ('name', 'email', 'assigned_user', 'date_created', NewCustomerListFilter)

    list_display = (
            'name',
            'email',
            'assigned_user',
            'new_customer',
            )

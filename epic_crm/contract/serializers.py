from rest_framework.serializers import ModelSerializer

from .models import Contract
from epic_crm.customer.serializers import CustomerSerializerList


class ContractSerializerList(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'customer', 'amount', 'date_signed']


class ContractSerializerDetails(ModelSerializer):

    customer = CustomerSerializerList()

    class Meta:
        model = Contract
        fields = ['pk', 'date_signed', 'date_created', 'date_updated',
                  'amount', 'information', 'customer', 'is_signed']


class ContractSerializerCreate(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'date_signed', 'amount', 'information', 'customer']


class ContractSerializerUpdateBySalesPeople(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['pk', 'date_signed', 'amount', 'information', 'customer']
        read_only_fields = ['customer']

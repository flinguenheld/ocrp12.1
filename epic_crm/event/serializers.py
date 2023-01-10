from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Event
from epic_crm.user.serializers import UserSerializerList
from epic_crm.contract.serializers import ContractSerializerList


class EventSerializerList(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'date', 'contract', 'assigned_user']


class EventSerializerDetails(ModelSerializer):

    contract = ContractSerializerList()
    assigned_user = UserSerializerList()

    class Meta:
        model = Event
        fields = ['pk', 'name', 'information', 'date', 'date_created', 'date_updated', 'contract', 'assigned_user']


class EventSerializerCreateByStaff(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'information', 'date', 'contract', 'assigned_user']


class EventSerializerCreateByCustomerAssignedUser(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'information', 'date', 'contract', 'assigned_user']
        read_only_fields = ['assigned_user']

    def validate_contract(self, value):
        if not value.is_signed:
            raise ValidationError('You cannot create an event if the contract has not been signed')

        return value


class EventSerializerUpdateByAssignedUser(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'information', 'date', 'contract', 'assigned_user']
        read_only_fields = ['contract', 'assigned_user']

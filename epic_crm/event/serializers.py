from rest_framework.serializers import ModelSerializer

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
        fields = ['pk', 'name', 'informations', 'date', 'date_created', 'date_updated', 'contract', 'assigned_user']


class EventSerializerCreateByStaff(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'informations', 'date', 'contract', 'assigned_user']


class EventSerializerCreateByCustomerAssignedUser(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'informations', 'date', 'contract', 'assigned_user']
        read_only_fields = ['assigned_user']


class EventSerializerUpdateByAssignedUser(ModelSerializer):

    class Meta:
        model = Event
        fields = ['pk', 'name', 'informations', 'date', 'contract', 'assigned_user']
        read_only_fields = ['contract', 'assigned_user']

from rest_framework.serializers import ModelSerializer

from .models import Customer
from epic_crm.user.serializers import UserSerializerList


class CustomerSerializerList(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'email', 'new_customer']


class CustomerSerializerDetails(ModelSerializer):

    assigned_user = UserSerializerList()

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'address', 'email', 'phone', 'mobile',
                  'date_created', 'assigned_user', 'new_customer']


class CustomerSerializerCreateByStaff(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'address', 'email', 'phone', 'mobile', 'assigned_user']


class CustomerSerializerCreate(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'address', 'email', 'phone', 'mobile', 'assigned_user']
        read_only_fields = ['assigned_user']

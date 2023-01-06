from rest_framework.serializers import ModelSerializer

from .models import Customer
from epic_crm.user.serializers import UserSerializerList


class CustomerSerializerList(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'email']


class CustomerSerializerDetails(ModelSerializer):

    affected_user = UserSerializerList()

    class Meta:
        model = Customer
        fields = ['pk', 'name', 'address', 'email', 'phone', 'mobile', 'date_created', 'affected_user']


class CustomerSerializerCreate(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'name', 'address', 'email', 'phone', 'mobile', 'date_created']

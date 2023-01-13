from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserSerializerList(ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username']


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ['name']


class UserSerializerDetails(ModelSerializer):

    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login', 'is_staff', 'groups']


class UserSerializerCreate(ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff']
        ReadOnlyFields = ['password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializerUpdate(ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name']

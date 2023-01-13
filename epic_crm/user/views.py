from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.contrib.auth.models import Group
from rest_framework.decorators import action

import django_filters

from . import serializers


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'contains'],
            'email': ['exact', 'contains'],
            'groups__name': ['exact']
        }


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True).order_by('username')

    def get_permissions(self):

        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.UserSerializerList

            case 'retrieve':
                return serializers.UserSerializerDetails

            case 'create':
                return serializers.UserSerializerCreate

            case 'update':
                return serializers.UserSerializerUpdate

    # --
    @action(methods=['put'], detail=True, permission_classes=[IsAdminUser])
    def set_manager(self, request, pk=None):
        return self._set_group(pk=pk, group_name='manager')

    @action(methods=['put'], detail=True, permission_classes=[IsAdminUser])
    def set_sales(self, request, pk=None):
        return self._set_group(pk=pk, group_name='sales')

    def _set_group(self, pk, group_name):

        user = get_object_or_404(User, pk=pk)
        group = Group.objects.get(name=group_name)

        if not user.groups.filter(name=group_name):
            user.groups.add(group)
            return Response({'detail': f'User has been hadded in the group {group_name}'})
        else:
            user.groups.remove(group)
            return Response({'detail': f'User has been removed in the group {group_name}'})

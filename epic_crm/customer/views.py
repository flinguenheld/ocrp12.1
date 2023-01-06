from rest_framework import mixins
from rest_framework import viewsets
import django_filters

from .models import Customer
from . import serializers

from rest_framework.permissions import DjangoModelPermissions
from .permissions import IsAssignedOrStaff


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'contains'],
            'email': ['exact', 'contains'],
        }


class CustomerViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    filterset_class = CustomerFilter
    permission_classes = [DjangoModelPermissions, IsAssignedOrStaff]

    def get_queryset(self):
        return Customer.objects.all().order_by('name')

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return serializers.CustomerSerializerList

            case 'retrieve':
                return serializers.CustomerSerializerDetails

            case 'create' | 'update':
                return serializers.CustomerSerializerCreate

    def perform_create(self, serializer):
        serializer.save(affected_user=self.request.user)
        serializer.save()

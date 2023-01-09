from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import django_filters

from .models import Contract
from . import serializers
from .permissions import IsAssignedOrStaff, IsAssignedOrStaffObject


class ContractFilter(django_filters.FilterSet):
    class Meta:
        model = Contract
        fields = {
            'customer__name': ['exact', 'contains'],
            'customer__email': ['exact', 'contains'],
            'amount': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'date_signed': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class ContractViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    filterset_class = ContractFilter

    def get_queryset(self):
        return Contract.objects.all().order_by('date_signed')

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            case 'create':
                permission_classes.append(IsAssignedOrStaff)

            case 'update':
                permission_classes.append(IsAssignedOrStaffObject)

            case 'destroy':
                permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return serializers.ContractSerializerList

            case 'retrieve':
                return serializers.ContractSerializerDetails

            case 'create':
                return serializers.ContractSerializerCreate

            case 'update':
                if self.request.user.is_staff:
                    return serializers.ContractSerializerCreate
                else:
                    return serializers.ContractSerializerUpdateBySalesPeople

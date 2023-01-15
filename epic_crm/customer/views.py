from rest_framework import mixins
from rest_framework import viewsets
import django_filters

from .models import Customer
from . import serializers

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAssignedOrStaff, CanAddCustomerOrStaff


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

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            case 'update':
                permission_classes.append(IsAssignedOrStaff)

            case 'create':
                permission_classes.append(CanAddCustomerOrStaff)

            case 'destroy':
                permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Customer.objects.all().order_by('name')

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return serializers.CustomerSerializerList

            case 'retrieve':
                return serializers.CustomerSerializerDetails

            case 'create' | 'update':
                if self.request.user.is_staff:
                    return serializers.CustomerSerializerCreateByStaff

                return serializers.CustomerSerializerCreate

    def perform_create(self, serializer):
        """ Auto assign the creator if he's not admin """
        if self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(assigned_user=self.request.user)

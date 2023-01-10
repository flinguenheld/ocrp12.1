from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import django_filters

from .models import Event
from . import serializers
from .permissions import IsAssignedToThisCustomerOrStaff, IsAssignedToThisEventOrStaff


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'contract__customer__name': ['exact', 'contains'],
            'contract__customer__email': ['exact', 'contains'],
            'date': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }


class EventViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):

    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.all().order_by('name')

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        match self.action:
            case 'create':
                permission_classes.append(IsAssignedToThisCustomerOrStaff)

            case 'update':
                permission_classes.append(IsAssignedToThisEventOrStaff)

            case 'destroy':
                permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        match self.action:
            case 'list':
                return serializers.EventSerializerList

            case 'retrieve':
                return serializers.EventSerializerDetails

            case 'create':
                if self.request.user.is_staff:
                    return serializers.EventSerializerCreateByStaff
                else:
                    return serializers.EventSerializerCreateByCustomerAssignedUser

            case 'update':
                if self.request.user.is_staff:
                    return serializers.EventSerializerCreateByStaff
                else:
                    return serializers.EventSerializerUpdateByAssignedUser

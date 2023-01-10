import pytest

from django.contrib.auth.models import User

from epic_crm.event.models import Event
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestEventsWithAssignedUser:

    def test_assigned_user_can_update_his_event(self, client_user_sophie):

        sophie = User.objects.get(username='Sophie')
        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)

        event = Event.objects.create(name='name event 0',
                                     date='2020-10-20T00:00:00Z',
                                     contract=contract,
                                     assigned_user=sophie)

        # --
        body = {'name': 'updated name',
                'date': '2023-10-20T00:00:00Z',
                'information': 'Some information'}

        response = client_user_sophie.put(f'/events/{event.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'updated name'
        assert data['date'] == '2023-10-20T00:00:00Z'
        assert data['information'] == 'Some information'
        assert data['contract'] == contract.pk
        assert data['assigned_user'] == sophie.pk

    def test_assigned_user_cannot_delete_his_event(self, client_user_sophie):

        sophie = User.objects.get(username='Sophie')
        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)

        event = Event.objects.create(name='name event 0',
                                     date='2020-10-20T00:00:00Z',
                                     contract=contract,
                                     assigned_user=sophie)

        # --
        response = client_user_sophie.delete(f'/events/{event.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

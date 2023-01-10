import pytest

from django.contrib.auth.models import User

from epic_crm.event.models import Event
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestEventsWithAssignedUser:

    def test_assigned_user_can_update_his_event(self, client_user_sophie, client_sales_mireille):

        sophie = User.objects.get(username='Sophie')
        mireille = User.objects.get(username='Mireille')

        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500, customer=customer)

        event = Event.objects.create(name='name event 0',
                                     date='2020-10-20T00:00:00Z',
                                     contract=contract,
                                     assigned_user=sophie)

        print(sophie.event_of.all())
        print(sophie.event_of.filter(pk=event.pk))

        # --
        body = {'name': 'updated name',
                'date': '2023-10-20T00:00:00Z',
                'informations': 'Some information'}

        response = client_user_sophie.put(f'/events/{event.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'updated name'
        assert data['date'] == '2023-10-20T00:00:00Z'
        assert data['informations'] == 'Some information'
        assert data['contract'] == contract.pk
        assert data['assigned_user'] == sophie.pk

    # def test_assigned_user_cannot_delete_his_event(self, client_sales_mireille):

        # mireille = User.objects.get(username='Mireille')
        # customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        # contract = Contract.objects.create(amount=1500, customer=customer)
        # event = Event.objects.create(name='name event 0', date='2020-10-20T00:00:00Z', contract=contract)

        # # --
        # response = client_sales_mireille.delete(f'/events/{event.pk}/')
        # data = response.json()

        # assert response.status_code == 403
        # assert 'You do not have permission to perform this action.' in data['detail']

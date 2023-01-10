import pytest

from django.contrib.auth.models import User

from epic_crm.event.models import Event
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestEventsWithCustomerAssignedUser:

    def test_customer_assigned_user_can_create_an_event_for_his_customer(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500, customer=customer)

        # --
        body = {'name': 'new event', 'date': '2023-10-20T00:00:00Z', 'contract': contract.pk}

        response = client_sales_mireille.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == 'new event'
        assert data['date'] == '2023-10-20T00:00:00Z'
        assert data['contract'] == contract.pk
        assert data['assigned_user'] is None

    def test_customer_assigned_user_cannot_update_his_customer_event(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500, customer=customer)

        event = Event.objects.create(name='name event 0',
                                     date='2020-10-20T00:00:00Z',
                                     contract=contract)

        # --
        body = {'name': 'updated name',
                'date': '2023-10-20T00:00:00Z',
                'information': 'Some information'}

        response = client_sales_mireille.put(f'/events/{event.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned user or staff are authorized.' in data['detail']

    def test_customer_assigned_user_cannot_delete_his_customer_event(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500, customer=customer)

        event = Event.objects.create(name='name event 0',
                                     date='2020-10-20T00:00:00Z',
                                     contract=contract)

        # --
        response = client_sales_mireille.delete(f'/events/{event.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

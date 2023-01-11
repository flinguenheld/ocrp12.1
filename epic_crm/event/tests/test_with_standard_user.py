import pytest

from epic_crm.event.models import Event
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestEvents:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/events/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_user_can_list_events(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')

        contract_0 = Contract.objects.create(amount=1500, customer=customer)
        contract_1 = Contract.objects.create(amount=3300.44, customer=customer)

        Event.objects.create(name='name event 0', date='2020-10-20', contract=contract_1)
        Event.objects.create(name='name event 1', date='2015-05-15', contract=contract_0)

        # --
        response = client_user_sophie.get('/events/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == 'name event 0'
        assert data[1]['name'] == 'name event 1'

    def test_user_can_get_event_details(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)
        event = Event.objects.create(name='name event 0', date='2020-10-20', contract=contract)

        # --
        response = client_user_sophie.get(f'/events/{event.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'name event 0'
        assert data['date'] == '2020-10-20'
        assert data['contract']['pk'] == contract.pk

    def test_user_cannot_create_an_event(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)

        # --
        body = {'name': 'new event', 'date': '2023-10-20', 'contract': contract.pk}

        response = client_user_sophie.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the customer assigned user or staff are authorized.' in data['detail']

    def test_user_cannot_update_an_event(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)
        event = Event.objects.create(name='name event 0', date='2020-10-20', contract=contract)

        # --
        body = {'name': 'updated name', 'date': '2023-10-20', 'contract': contract.pk}

        response = client_user_sophie.put(f'/events/{event.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned user or staff are authorized.' in data['detail']

    def test_user_cannot_delete_an_event(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)
        event = Event.objects.create(name='name event 0', date='2020-10-20', contract=contract)

        # --
        response = client_user_sophie.delete(f'/events/{event.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

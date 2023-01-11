import pytest

from django.contrib.auth.models import User

from epic_crm.event.models import Event
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestEventsWithStaff:

    def test_staff_can_create_an_event(self, client_staff_jean):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)

        # --
        body = {'name': 'new event',
                'date': '2023-10-20',
                'contract': contract.pk,
                'assigned_user': user.pk}

        response = client_staff_jean.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == 'new event'
        assert data['date'] == '2023-10-20'
        assert data['contract'] == contract.pk
        assert data['assigned_user'] == user.pk

    def test_staff_can_update_an_event(self, client_staff_jean):

        user = User.objects.create_user(username='aaaaa', password='test01234')

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)
        event = Event.objects.create(name='name event 0', date='2020-10-20', contract=contract)

        # --
        body = {'name': 'updated name',
                'date': '2023-10-20',
                'contract': contract.pk,
                'assigned_user': user.pk}

        response = client_staff_jean.put(f'/events/{event.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'updated name'
        assert data['date'] == '2023-10-20'
        assert data['contract'] == contract.pk
        assert data['assigned_user'] == user.pk

    def test_staff_can_delete_an_event(self, client_staff_jean):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500, customer=customer)
        event = Event.objects.create(name='name event 0', date='2020-10-20', contract=contract)

        # --
        response = client_staff_jean.delete(f'/events/{event.pk}/')

        assert response.status_code == 204
        assert Event.objects.count() == 0

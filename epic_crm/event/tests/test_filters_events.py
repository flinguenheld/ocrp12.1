import pytest

from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract
from epic_crm.event.models import Event


@pytest.mark.django_db
class TestEventsFilters:

    def test_events_without_filter(self, client_user_sophie):

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(customer=customer_c)
        Event.objects.create(name='event c', contract=contract_c, date='2025-05-25T00:00:00Z')

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(customer=customer_a)
        Event.objects.create(name='event a', contract=contract_a, date='2015-05-15T00:00:00Z')

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(customer=customer_b)
        Event.objects.create(name='event b', contract=contract_b, date='2020-02-20T00:00:00Z')

        # --
        response = client_user_sophie.get('/events/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['name'] == 'event a'
        assert data[1]['name'] == 'event b'
        assert data[2]['name'] == 'event c'

    def test_events_filter_by_customer_name(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(customer=customer_a)
        Event.objects.create(name='event a', contract=contract_a, date='2015-05-15T00:00:00Z')

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(customer=customer_b)
        Event.objects.create(name='event b', contract=contract_b, date='2020-02-20T00:00:00Z')

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(customer=customer_c)
        Event.objects.create(name='event c', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = client_user_sophie.get('/events/?contract__customer__name=aaaa')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'event a'

    def test_events_filter_by_customer_email(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(customer=customer_a)
        Event.objects.create(name='event a', contract=contract_a, date='2015-05-15T00:00:00Z')

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(customer=customer_b)
        Event.objects.create(name='event b', contract=contract_b, date='2020-02-20T00:00:00Z')

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(customer=customer_c)
        Event.objects.create(name='event c', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = client_user_sophie.get('/events/?contract__customer__email__contains=b@')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'event b'

    def test_events_filter_by_date(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(customer=customer_a)
        Event.objects.create(name='event a', contract=contract_a, date='2015-05-15T00:00:00Z')

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(customer=customer_b)
        Event.objects.create(name='event b', contract=contract_b, date='2020-02-20T00:00:00Z')

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(customer=customer_c)
        Event.objects.create(name='event c', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = client_user_sophie.get('/events/?date=2020-02-20')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'event b'

        response = client_user_sophie.get('/events/?date__gte=2018-02-20')
        data = response.json()

        assert len(data) == 2
        assert data[0]['name'] == 'event b'
        assert data[1]['name'] == 'event c'

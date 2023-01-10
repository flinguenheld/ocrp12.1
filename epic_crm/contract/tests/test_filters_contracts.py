import pytest

from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestContractFilters:

    def test_contracts_without_filter(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(customer=customer_a, amount=100)

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(customer=customer_b, amount=200)

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(customer=customer_c, amount=300)

        # --
        response = client_user_sophie.get('/contracts/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['amount'] == '100.00'
        assert data[1]['amount'] == '200.00'
        assert data[2]['amount'] == '300.00'

    def test_contracts_filter_by_client_name(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(customer=customer_a, amount=100)

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(customer=customer_b, amount=200)

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(customer=customer_c, amount=300)

        # --
        response = client_user_sophie.get('/contracts/?customer__name=bbbb')
        data = response.json()

        assert len(data) == 1
        assert data[0]['amount'] == '200.00'

    def test_contracts_filter_by_client_email(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(customer=customer_a, amount=100)

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(customer=customer_b, amount=200)

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(customer=customer_c, amount=300)

        # --
        response = client_user_sophie.get('/contracts/?customer__email__contains=b')
        data = response.json()

        assert len(data) == 1
        assert data[0]['amount'] == '200.00'

    def test_contracts_filter_by_amount(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(customer=customer_a, amount=100)

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(customer=customer_b, amount=200)

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(customer=customer_c, amount=300)

        # --
        response = client_user_sophie.get('/contracts/?amount=300')
        data = response.json()

        assert len(data) == 1
        assert data[0]['amount'] == '300.00'

        response = client_user_sophie.get('/contracts/?amount__lte=200')
        data = response.json()

        assert len(data) == 2
        assert data[0]['amount'] == '100.00'
        assert data[1]['amount'] == '200.00'

    def test_contracts_filter_by_date_signed(self, client_user_sophie):

        customer_a = Customer.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(customer=customer_a, date_signed='2010-10-10T00:00:00Z', amount=100)

        customer_b = Customer.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(customer=customer_b, date_signed='2015-05-15T00:00:00Z', amount=200)

        customer_c = Customer.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(customer=customer_c, date_signed='2020-02-20T00:00:00Z', amount=300)

        # --
        response = client_user_sophie.get('/contracts/?date_signed=2020-02-20')
        data = response.json()

        assert len(data) == 1
        assert data[0]['amount'] == '300.00'

        response = client_user_sophie.get('/contracts/?date_signed__lte=2016-06-16')
        data = response.json()

        assert len(data) == 2
        assert data[0]['amount'] == '100.00'
        assert data[1]['amount'] == '200.00'

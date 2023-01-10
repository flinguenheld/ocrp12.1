import pytest

from epic_crm.customer.models import Customer


@pytest.mark.django_db
class TestCustomerFilters:

    def test_customers_without_filter(self, client_user_sophie):

        Customer.objects.create(name='aaaa')
        Customer.objects.create(name='bbbb')
        Customer.objects.create(name='cccc')

        # --
        response = client_user_sophie.get('/customers/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['name'] == 'aaaa'
        assert data[1]['name'] == 'bbbb'
        assert data[2]['name'] == 'cccc'

    def test_customers_filter_by_name(self, client_user_sophie):

        Customer.objects.create(name='aaaa')
        Customer.objects.create(name='bbbb')
        Customer.objects.create(name='cccc')

        # --
        response = client_user_sophie.get('/customers/?name__contains=b')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'bbbb'

    def test_customers_filter_by_email(self, client_user_sophie):

        Customer.objects.create(name='aaaa', email='a@a.com')
        Customer.objects.create(name='bbbb', email='b@b.com')
        Customer.objects.create(name='cccc', email='c@c.com')

        # --
        response = client_user_sophie.get('/customers/?email=c@c.com')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'cccc'
        assert data[0]['email'] == 'c@c.com'

import pytest

from django.contrib.auth.models import User

from epic_crm.customer.models import Customer


@pytest.mark.django_db
class TestCustomers:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/customers/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_user_can_list_customers(self, client_user):

        Customer.objects.create(name='name 0')
        Customer.objects.create(name='name 1')

        # --
        response = client_user.get('/customers/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == 'name 0'
        assert data[1]['name'] == 'name 1'

    def test_user_can_get_client_details(self, client_user):

        customer = Customer.objects.create(name='name 0', mobile='001122334455')

        # --
        response = client_user.get(f'/customers/{customer.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'name 0'
        assert data['mobile'] == '001122334455'

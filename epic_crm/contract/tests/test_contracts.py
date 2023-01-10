import pytest

from django.contrib.auth.models import User

from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract


@pytest.mark.django_db
class TestContracts:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/contracts/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_user_can_list_contracts(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        Contract.objects.create(amount=1500, customer=customer)
        Contract.objects.create(amount=3300.44, customer=customer)

        # --
        response = client_user_sophie.get('/contracts/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['amount'] == '1500.00'
        assert data[1]['amount'] == '3300.44'

    def test_user_can_get_contract_details(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500.00, customer=customer, date_signed='2015-05-15T00:00:00Z')

        # --
        response = client_user_sophie.get(f'/contracts/{contract.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['amount'] == '1500.00'
        assert data['customer']['name'] == 'name 0'
        assert data['is_signed'] is True

    def test_user_cannot_create_a_contract(self, client_user_sophie):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='name 0', assigned_user=user)

        # --
        body = {'amount': 1500, 'customer': customer.pk}

        response = client_user_sophie.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned user or staff are authorized' in data['detail']

    def test_staff_can_create_a_contract(self, client_staff_jean):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='name 0', assigned_user=user)

        # --
        body = {'amount': 1500.00, 'customer': customer.pk}

        response = client_staff_jean.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['amount'] == '1500.00'
        assert data['customer'] == customer.pk

    def test_assigned_user_can_create_a_contract_for_his_customer(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)

        # --
        body = {'amount': 1500.00, 'customer': customer.pk}

        response = client_sales_mireille.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['amount'] == '1500.00'
        assert data['customer'] == customer.pk
        assert Customer.objects.get(pk=data['customer']).assigned_user == mireille

    def test_user_cannot_update_a_contract(self, client_user_sophie):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='name 0', assigned_user=user)
        contract = Contract.objects.create(amount=1500.00, customer=customer, date_signed='2015-05-15T00:00:00Z')

        # --
        body = {'amount': 1500.00, 'information': 'blablabla'}

        response = client_user_sophie.put(f'/contracts/{contract.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned user or staff are authorized' in data['detail']

    def test_staff_can_update_a_contract(self, client_staff_jean):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='name 0', assigned_user=user)
        contract = Contract.objects.create(amount=1500.00, customer=customer, date_signed='2015-05-15T00:00:00Z')

        # --
        body = {'amount': 3333.33, 'information': 'blablabla', 'customer': customer.pk}

        response = client_staff_jean.put(f'/contracts/{contract.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['date_signed'] == '2015-05-15T00:00:00Z'
        assert data['amount'] == '3333.33'
        assert data['customer'] == customer.pk

    def test_assigned_user_can_update_his_contract(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500.00, customer=customer, date_signed='2015-05-15T00:00:00Z')

        # --
        body = {'amount': 3333.33, 'information': 'blablabla', 'date_signed': '2020-06-10'}

        response = client_sales_mireille.put(f'/contracts/{contract.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['date_signed'] == '2020-06-10T00:00:00Z'
        assert data['amount'] == '3333.33'
        assert data['information'] == 'blablabla'

    def test_user_cannot_delete_a_contract(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500.00, customer=customer)

        # --
        response = client_user_sophie.delete(f'/contracts/{contract.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_assigned_user_cannot_delete_a_contract_with_his_customer(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='name 0', assigned_user=mireille)
        contract = Contract.objects.create(amount=1500.00, customer=customer)

        # --
        response = client_sales_mireille.delete(f'/contracts/{contract.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_staff_can_delete_a_contract(self, client_staff_jean):

        customer = Customer.objects.create(name='name 0')
        contract = Contract.objects.create(amount=1500.00, customer=customer)

        # --
        response = client_staff_jean.delete(f'/contracts/{contract.pk}/')

        assert response.status_code == 204
        assert Contract.objects.count() == 0

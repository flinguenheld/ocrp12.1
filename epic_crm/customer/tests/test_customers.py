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

    def test_user_can_list_customers(self, client_user_sophie):

        Customer.objects.create(name='name 0')
        Customer.objects.create(name='name 1')

        # --
        response = client_user_sophie.get('/customers/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == 'name 0'
        assert data[1]['name'] == 'name 1'

    def test_user_can_get_customer_details(self, client_user_sophie):

        customer = Customer.objects.create(name='name 0', mobile='001122334455')

        # --
        response = client_user_sophie.get(f'/customers/{customer.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'name 0'
        assert data['mobile'] == '001122334455'

    def test_user_cannot_create_a_customer(self, client_user_sophie):

        body = {'name': 'Test name',
                'phone': '0600000000'}

        response = client_user_sophie.post('/customers/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only salespeople or staff are authorized' in data['detail']

    def test_staff_can_create_a_customer(self, client_staff_jean):

        body = {'name': 'Test name',
                'phone': '0600000000'}

        response = client_staff_jean.post('/customers/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == 'Test name'
        assert data['phone'] == '0600000000'
        assert data['assigned_user'] == User.objects.get(username='Jean').pk

    def test_user_in_group_sales_can_create_a_customer(self, client_sales_mireille):

        body = {'name': 'Test name',
                'phone': '0600000000'}

        response = client_sales_mireille.post('/customers/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == 'Test name'
        assert data['phone'] == '0600000000'

        # Check the auto user assignement
        Customer.objects.get(name='Test name').assigned_user = User.objects.get(username='Mireille')

    def test_user_cannot_update_a_customer(self, client_user_sophie):

        customer = Customer.objects.create(name='Test name', phone='1111111111')

        # --
        body = {'name': 'Test name',
                'phone': '0600000000'}

        response = client_user_sophie.put(f'/customers/{customer.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned user or staff are authorized' in data['detail']

    def test_staff_can_update_a_customer(self, client_staff_jean):

        user = User.objects.create_user(username='aaaaa', password='test01234')
        customer = Customer.objects.create(name='Test name', phone='1111111111')

        # --
        body = {'name': 'Updated name',
                'phone': '22222222222',
                'assigned_user': user.pk}

        response = client_staff_jean.put(f'/customers/{customer.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Updated name'
        assert data['phone'] == '22222222222'
        assert data['email'] == ''
        assert data['assigned_user'] == user.pk

    def test_assigned_user_can_update_his_customer(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='Test name', phone='1111111111', assigned_user=mireille)

        # --
        body = {'name': 'Updated name',
                'phone': '22222222222'}

        response = client_sales_mireille.put(f'/customers/{customer.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Updated name'
        assert data['phone'] == '22222222222'
        assert data['email'] == ''
        assert data['assigned_user'] == mireille.pk

    def test_user_cannot_delete_a_customer(self, client_user_sophie):

        customer = Customer.objects.create(name='Test name', phone='1111111111')

        # --
        response = client_user_sophie.delete(f'/customers/{customer.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_assigned_user_cannot_delete_his_customer(self, client_sales_mireille):

        mireille = User.objects.get(username='Mireille')
        customer = Customer.objects.create(name='Test name', phone='1111111111', assigned_user=mireille)

        # --
        response = client_sales_mireille.delete(f'/customers/{customer.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_staff_can_delete_a_customer(self, client_staff_jean):

        customer = Customer.objects.create(name='Test name', phone='1111111111')

        # --
        response = client_staff_jean.delete(f'/customers/{customer.pk}/')

        assert response.status_code == 204
        assert Customer.objects.count() == 0

import pytest
from django.contrib.auth.models import User

from epic_crm.user.groups import init_groups
from epic_crm.customer.models import Customer
from epic_crm.contract.models import Contract
from epic_crm.event.models import Event


@pytest.mark.django_db
class TestUsersExtraRoutes:

    def test_user_can_list_assigned_customer_users(self, client_user_sophie):

        User.objects.create_user(username='roger', password='test01234')
        User.objects.create_user(username='marcel', password='test01234')

        igor = User.objects.create_user(username='igor', password='test01234')
        camille = User.objects.create_user(username='camille', password='test01234')

        Customer.objects.create(name='customer 0', assigned_user=igor)
        Customer.objects.create(name='customer 1', assigned_user=camille)

        # --
        response = client_user_sophie.get('/users/list_salespeople/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]['username'] == 'igor'
        assert data[1]['username'] == 'camille'

    def test_user_can_list_assigned_event_users(self, client_user_sophie):

        roger = User.objects.create_user(username='roger', password='test01234')
        marcel = User.objects.create_user(username='marcel', password='test01234')

        igor = User.objects.create_user(username='igor', password='test01234')
        camille = User.objects.create_user(username='camille', password='test01234')

        customer_0 = Customer.objects.create(name='customer 0', assigned_user=igor)
        contract_0 = Contract.objects.create(amount=1500, customer=customer_0, date_signed='2020-10-20')
        Event.objects.create(name='name event 0', date='2020-10-20', contract=contract_0, assigned_user=roger)

        customer_1 = Customer.objects.create(name='customer 1', assigned_user=camille)
        contract_1 = Contract.objects.create(amount=1500, customer=customer_1, date_signed='2020-10-20')
        Event.objects.create(name='name event 1', date='2020-10-20', contract=contract_1, assigned_user=marcel)

        # --
        response = client_user_sophie.get('/users/list_technicians/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]['username'] == 'roger'
        assert data[1]['username'] == 'marcel'

    def test_user_cannot_add_nor_remove_groups_to_a_user(self, client_user_sophie):

        init_groups()
        user = User.objects.create_user(username='name_0', password='test01234')

        # --
        response = client_user_sophie.put(f'/users/{user.pk}/set_sales/')
        data = response.json()

        assert 'You do not have permission to perform this action.' in data['detail']
        assert not user.groups.filter(name='sales')

        # --
        response = client_user_sophie.put(f'/users/{user.pk}/set_manager/')
        data = response.json()

        assert 'You do not have permission to perform this action.' in data['detail']
        assert not user.groups.filter(name='manager')

    def test_staff_can_add_and_remove_group_sales_to_a_user(self, client_staff_jean):

        init_groups()
        user = User.objects.create_user(username='name_0', password='test01234')

        # --
        response = client_staff_jean.put(f'/users/{user.pk}/set_sales/')
        data = response.json()

        assert 'User has been hadded in the group sales' in data['detail']
        assert user.groups.filter(name='sales')

        # --
        response = client_staff_jean.put(f'/users/{user.pk}/set_sales/')
        data = response.json()

        assert 'User has been removed in the group sales' in data['detail']
        assert not user.groups.filter(name='sales')

    def test_staff_can_add_and_remove_group_manager_to_a_user(self, client_staff_jean):

        init_groups()
        user = User.objects.create_user(username='name_0', password='test01234')

        # --
        response = client_staff_jean.put(f'/users/{user.pk}/set_manager/')
        data = response.json()

        assert 'User has been hadded in the group manager' in data['detail']
        assert user.groups.filter(name='manager')

        # --
        response = client_staff_jean.put(f'/users/{user.pk}/set_manager/')
        data = response.json()

        assert 'User has been removed in the group manager' in data['detail']
        assert not user.groups.filter(name='manager')

import pytest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from epic_crm.user.groups import init_groups


@pytest.mark.django_db
class TestUsersFilters:

    def test_users_without_filter(self, client_user_sophie):

        User.objects.create_user(username='aaaa', password='test01234')
        User.objects.create_user(username='bbbb', password='test01234')
        User.objects.create_user(username='cccc', password='test01234')

        # --
        response = client_user_sophie.get('/users/')
        data = response.json()

        assert len(data) == 4
        assert data[0]['username'] == 'aaaa'
        assert data[1]['username'] == 'bbbb'
        assert data[2]['username'] == 'cccc'
        assert data[3]['username'] == 'Sophie'

    def test_users_filter_by_username(self, client_user_sophie):

        User.objects.create_user(username='aaaa', password='test01234')
        User.objects.create_user(username='bbbb', password='test01234')
        User.objects.create_user(username='cccc', password='test01234')

        # --
        response = client_user_sophie.get('/users/?username=aaaa')
        data = response.json()

        assert len(data) == 1
        assert data[0]['username'] == 'aaaa'

    def test_users_filter_by_user_email(self, client_user_sophie):

        User.objects.create_user(username='aaaa', password='test01234', email='a@a.com')
        User.objects.create_user(username='bbbb', password='test01234', email='b@b.com')
        User.objects.create_user(username='cccc', password='test01234', email='c@c.com')

        # --
        response = client_user_sophie.get('/users/?email__contains=b@')
        data = response.json()

        assert len(data) == 1
        assert data[0]['username'] == 'bbbb'

    def test_users_filter_by_groups_sales_and_manager(self, client_user_sophie):

        init_groups()

        group_sales = Group.objects.get(name='sales')
        group_manager = Group.objects.get(name='manager')

        user_a = User.objects.create_user(username='aaaa', password='test01234', email='a@a.com')
        user_b = User.objects.create_user(username='bbbb', password='test01234', email='b@b.com')
        user_c = User.objects.create_user(username='cccc', password='test01234', email='c@c.com')

        user_a.groups.add(group_sales)
        user_b.groups.add(group_sales)

        user_b.groups.add(group_manager)
        user_c.groups.add(group_manager)

        # --
        response = client_user_sophie.get('/users/?groups__name=sales')
        data = response.json()

        assert len(data) == 2
        assert data[0]['username'] == 'aaaa'
        assert data[1]['username'] == 'bbbb'

        response = client_user_sophie.get('/users/?groups__name=manager')
        data = response.json()

        assert len(data) == 2
        assert data[0]['username'] == 'bbbb'
        assert data[1]['username'] == 'cccc'

import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUsers:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/users/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_user_can_list_users(self, client_user_sophie):

        User.objects.create_user(username='name_0', password='test01234')
        User.objects.create_user(username='name_1', password='test01234')

        # --
        response = client_user_sophie.get('/users/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['username'] == 'name_0'
        assert data[1]['username'] == 'name_1'

    def test_user_can_get_customer_details(self, client_user_sophie):

        user = User.objects.create_user(username='name_0', password='test01234', email='a@a.com')

        # --
        response = client_user_sophie.get(f'/users/{user.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['username'] == 'name_0'
        assert data['email'] == 'a@a.com'

    def test_user_cannot_create_a_user(self, client_user_sophie):

        body = {'username': 'Sam',
                'password': 'test01234'}

        response = client_user_sophie.post('/users/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_staff_can_create_a_user(self, client_staff_jean):

        body = {'username': 'Sam',
                'password': 'test01234',
                'email': 'sam@test.com'}

        response = client_staff_jean.post('/users/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['username'] == 'Sam'
        assert data['email'] == 'sam@test.com'

    def test_user_cannot_update_a_user(self, client_user_sophie):

        user = User.objects.create_user(username='name_0', password='test01234', email='a@a.com')

        # --
        body = {'username': 'Sam',
                'email': 'sam@test.com',
                'first_name': 'Samuel',
                'last_name': 'Ronchant'}

        response = client_user_sophie.put(f'/users/{user.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_staff_can_update_a_user(self, client_staff_jean):

        user = User.objects.create_user(username='name_0', password='test01234', email='a@a.com')

        # --
        body = {'username': 'Sam',
                'email': 'sam@test.com',
                'first_name': 'Samuel',
                'last_name': 'Ronchant'}

        response = client_staff_jean.put(f'/users/{user.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['username'] == 'Sam'
        assert data['email'] == 'sam@test.com'
        assert data['first_name'] == 'Samuel'
        assert data['last_name'] == 'Ronchant'

    def test_user_cannot_delete_a_user(self, client_user_sophie):

        user = User.objects.create_user(username='name_0', password='test01234')

        # --
        response = client_user_sophie.delete(f'/users/{user.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'You do not have permission to perform this action.' in data['detail']

    def test_staff_can_delete_a_user(self, client_staff_jean):

        user = User.objects.create_user(username='name_0', password='test01234')

        # --
        response = client_staff_jean.delete(f'/users/{user.pk}/')

        assert response.status_code == 204
        assert User.objects.filter(username='name_0').count() == 0

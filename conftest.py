import pytest
import logging

from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group

from epic_crm.user.groups import init_groups

# Logging --
logger = logging.getLogger('django')


@pytest.fixture(scope="session", autouse=True)
def prout():
    logger.info('========================= PYTEST SESSION START =========================')
    yield
    logger.info('========================= PYTEST SESSION  END  =========================')


# --
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def client_staff_jean():

    user = User.objects.create_user(username='Jean', password='test01234')
    user.is_staff = True
    user.save()

    return connect('Jean')


@pytest.fixture
def client_user_sophie():

    User.objects.create_user(username='Sophie', password='test01234')
    return connect('Sophie')


@pytest.fixture
def client_sales_mireille():

    user = User.objects.create_user(username='Mireille', password='test01234')

    init_groups()
    user.groups.add(Group.objects.get(name='sales'))

    return connect('Mireille')


@pytest.fixture
def client_tech_patrick():

    user = User.objects.create_user(username='Patrick', password='test01234')

    init_groups()
    user.groups.add(Group.objects.get(name='tech'))

    return connect('Patrick')


# --
def connect(username):

    client = APIClient()
    response = client.post("/login/", data={"username": username, "password": 'test01234'})
    data = response.json()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access']}")
    return client

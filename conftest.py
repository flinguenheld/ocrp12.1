import pytest
import logging

from rest_framework.test import APIClient
from django.contrib.auth.models import User
# from epic_crm.users.models import UserRole


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
def api_client_manager():
    client = APIClient()
    return add_user_then_connect(client,
                                 username='admin',
                                 email='manager@pytest.com',
                                 password='test01234',
                                 role='Manager')


@pytest.fixture
def api_client_salesperson():
    client = APIClient()
    return add_user_then_connect(client,
                                 username='salesper',
                                 email='salesperson@pytest.com',
                                 password='test01234',
                                 role='Salesperson')


@pytest.fixture
def api_client_technical_support():
    client = APIClient()
    return add_user_then_connect(client,
                                 username='techni',
                                 email='technical_support@pytest.com',
                                 password='test01234',
                                 role='Technical support')


def add_user_then_connect(client, username, email, password, role):

    user = User.objects.create_user(username=username, email=email, password=password)
    user.role_of.role = role

    response = client.post("/login/", data={"username": username, "password": password})
    data = response.json()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access']}")
    return client

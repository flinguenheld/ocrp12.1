from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'customers', views.CustomerViewSet, basename='customers')
# /customers/{customer_pk}/


urlpatterns = [
    path('', include(router.urls)),
]

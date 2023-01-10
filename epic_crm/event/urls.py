from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'events', views.EventViewSet, basename='events')
# /events/{event_pk}/


urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')
# /users/{user_pk}/

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
]

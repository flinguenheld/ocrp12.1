from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', include('epic_crm.user.urls')),
    path('', include('epic_crm.customer.urls')),
    # path('', include('epic_crm.contract.urls')),
    # path('', include('epic_crm.event.urls')),
]

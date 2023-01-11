from django.contrib import admin
from django.urls import path, include

# from epic_crm.user.admin import manager_site


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # path('manager/', manager_site.urls),

    path('', include('epic_crm.user.urls')),
    path('', include('epic_crm.customer.urls')),
    path('', include('epic_crm.contract.urls')),
    path('', include('epic_crm.event.urls')),
]

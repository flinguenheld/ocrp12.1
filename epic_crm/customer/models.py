from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    name = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=300, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=100, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    assigned_user = models.ForeignKey(to=User,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      default=None,
                                      related_name='customer_of')

    @property
    def new_customer(self):
        return self.contract_of.exclude(date_signed=None).count() == 0

    def __str__(self):
        return f"Customer [ {self.pk} - {self.name} ]"

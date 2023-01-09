from django.db import models

from epic_crm.customer.models import Customer


class Contract(models.Model):

    date_signed = models.DateTimeField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateField(auto_now=True)

    amount = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)
    informations = models.CharField(max_length=500, blank=True)

    customer = models.ForeignKey(to=Customer,
                                 on_delete=models.CASCADE,
                                 related_name='contract_of')

    @property
    def is_signed(self):
        return self.date_signed is not None

    def __str__(self):
        return f"Contract [ {self.pk} - {self.customer} - {self.date_signed} ]"

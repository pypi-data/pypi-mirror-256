from django.db import models

from evercycle_models.models import Workflow, Address, Contact, ServiceOrderDevice


class ServiceOrder(models.Model):
    reference = models.CharField(max_length=100)
    ship_to_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    request_type = models.CharField(max_length=10)

    devices = models.ManyToManyField(ServiceOrderDevice)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    workflow_id = models.ForeignKey(Workflow, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'service_order'

from django.db import models


class ServiceOrder(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'service_order'

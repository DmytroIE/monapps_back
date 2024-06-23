from django.db import models
from apps.datastreams.models import Datastream


class Reading(models.Model):

    class Meta:
        db_table = "readings"

    timestamp = models.DateTimeField(blank=False, null=False, primary_key=True)
    datastream = models.ForeignKey(
        Datastream,
        on_delete=models.PROTECT,
    )
    reading = models.FloatField(null=True)

    def __str__(self):
        return f"Reading dev_id:{self.datastream.device.id} ds_id:{self.datastream.id} ts:{self.timestamp}"

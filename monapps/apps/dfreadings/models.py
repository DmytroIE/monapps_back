from django.db import models
from apps.datafeeds.models import Datafeed


class DfReading(models.Model):

    class Meta:
        db_table = "dfreadings"

    timestamp = models.DateTimeField(blank=False, null=False, primary_key=True)
    datafeed = models.ForeignKey(
        Datafeed,
        on_delete=models.PROTECT,
    )
    reading = models.FloatField(null=True)

    def __str__(self):
        return f"Df reading df_id:{self.datafeed.id} ts:{self.timestamp}"

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_celery_beat.models import PeriodicTask

class MonAppType(models.Model):
    class Meta:
        db_table = "dstypes"

    name = models.CharField(max_length=200, blank = False, unique = True)
    description = models.CharField(max_length=1000, blank = True)
    path = models.CharField(max_length=200, blank = False, unique = True)
    # version = models.CharField(max_length=10, blank = False, default='0.0.1')

    def __str__(self):
        return self.name


class MonApplication(models.Model):

    class Meta:
        db_table = "monapplications"

    STOPPED = 0
    RUNNING = 1
    ERROR = -1
    EXEC_STATE_CHOICES = {
        STOPPED: "Stopped",
        RUNNING: "Running",
        ERROR: "Error",
    }
    execution_state = models.IntegerField(
        choices=EXEC_STATE_CHOICES,
        default=STOPPED,
    )

    input_datastreams = ArrayField(models.BigIntegerField()) # ids of datastreams from the external db
    output_datastreams = ArrayField(models.BigIntegerField()) # ids of datastreams from the external db

    state = models.JSONField(null=True)

    task = models.OneToOneField(PeriodicTask, 
                             on_delete = models.SET_NULL,
                             null = True,
                             blank = True,
                             default = None)

    datastream = models.ForeignKey(
        MonAppType,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Mon app id:{self.id}"

import datetime
import json
import django.db
from django.db import models
from django_celery_beat.models import PeriodicTask
from apps.devices.models import Device

class DatastreamType(models.Model):
    class Meta:
        db_table = "dstypes"

    name = models.CharField(max_length=200, blank = False, unique = True)

    def __str__(self):
        return self.name

def SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT(collector, field, sub_objs, using):
# https://stackoverflow.com/questions/48322538/django-foreignkey-on-delete-set-default-behavior
    try:
        default_dstype = DatastreamType.objects.get(name='Unknown')
    except DatastreamType.DoesNotExist:
        raise django.db.InternalError("You should have default DatastreamType=Unknown before "
                                      "deleting a referenced DatastreamType")
    for item in sub_objs:
        if item.type == default_dstype:
            raise django.db.InternalError("You cannot delete default DatastreamType "
                                          "when there are items referencing it")

    collector.add_field_update(field, default_dstype, sub_objs)



class Datastream(models.Model):

    class Meta:
        db_table = "datastreams"

    type = models.ForeignKey(
        DatastreamType,
        on_delete = SET_DEFAULT_AND_PREVENT_DELETE_DEFAULT, # doesn't matter what to choose as all this is read-only
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    
    task = models.OneToOneField(PeriodicTask, 
                             on_delete = models.SET_NULL, # doesn't matter what to choose as all this is read-only
                             null = True,
                             blank = True,
                             default = None)

    is_query_perm = models.BooleanField(default = True)  # if True then the external consumer can query
    val_max = models.FloatField()
    val_min = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Datastream dev_id:{self.device.id} id:{self.id}'

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericRelation
from apps.nodes.models import Node

class DatafeedType(models.Model):
    class Meta:
        db_table = "dftypes"

    name = models.CharField(max_length=200, blank = False, unique = True)
    base_unit = models.ForeignKey('datafeeds.DfMeasUnit', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
class DfMeasUnit(models.Model):
    class Meta:
        db_table = "dfmeasunits"

    name = models.CharField(max_length=200, blank = False, unique = True)
    type = models.ForeignKey(DatafeedType, on_delete = models.CASCADE)
    conv_factor = models.FloatField(default=1.0) # used for conversion to the base unit

    def to_base_unit(self):
        return self.type.base_unit*self.conv_factor


    def __str__(self):
        return self.name
    

class Datafeed(models.Model):

    class Meta:
        db_table = "datafeeds"

    name = models.CharField(max_length=200)

    meas_unit = models.ForeignKey(DfMeasUnit, on_delete=models.PROTECT)
    node = GenericRelation(Node)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Datafeed {self.name} id: {self.id}'
    
    @property
    def type(self):
        return self.meas_unit.type

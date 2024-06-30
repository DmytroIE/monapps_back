from django.contrib import admin
from .models import Datafeed, DfMeasUnit, DatafeedType

admin.site.register(DfMeasUnit)
admin.site.register(DatafeedType)
admin.site.register(Datafeed)

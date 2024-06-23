from rest_framework import serializers

from .models import Datastream
from django_celery_beat.models import PeriodicTask


class PeriodicTaskNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ['interval', 'enabled']


class DatastreamSerializer(serializers.ModelSerializer):
    task = PeriodicTaskNestedSerializer()

    class Meta:
        model = Datastream
        fields = ['id', 'type', 'device', 'is_query_perm',
                  'val_max', 'val_min', 'task']

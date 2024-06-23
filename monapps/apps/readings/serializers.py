from rest_framework import serializers
from django.utils.timezone import datetime

from .models import Reading

class JsTimestampField(serializers.Field):
    """
    Datetime objects are serialized into JS timestamps.
    """
    def to_representation(self, value):
        return int(value.timestamp() * 1000)

    def to_internal_value(self, data):
        miliseconds = int(data)
        return datetime.fromtimestamp(miliseconds / 1000.0)



class ReadingSerializer(serializers.ModelSerializer):
    timestamp = JsTimestampField()
    class Meta:
        model = Reading
        fields = '__all__'
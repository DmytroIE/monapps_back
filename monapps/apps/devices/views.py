from .models import Device
from .serializers import DeviceSerializer
from rest_framework import generics


class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceRetrieve(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

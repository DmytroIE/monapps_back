from django.db.models import ProtectedError
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Datastream
from .serializers import DatastreamSerializer


class DatastreamList(generics.ListAPIView):
    queryset = Datastream.objects.all()
    serializer_class = DatastreamSerializer


class DatastreamRetrieve(generics.RetrieveAPIView):
    queryset = Datastream.objects.all()
    serializer_class = DatastreamSerializer

from rest_framework import viewsets
from testapp.models import hydjobs, punejobs, blorejobs, chennaijobs
from testapp.api.serializers import HydJobsSerializer, PuneJobsSerializer, ChennaiJobsSerializer, BloreJobsSerializer


class HydJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = HydJobsSerializer
    queryset = hydjobs.objects.all()


class PuneJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = PuneJobsSerializer
    queryset = punejobs.objects.all()


class ChennaiJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = ChennaiJobsSerializer
    queryset = chennaijobs.objects.all()


class BloreJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = BloreJobsSerializer
    queryset = blorejobs.objects.all()

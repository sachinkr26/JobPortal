from django.contrib.sites import requests
from django.middleware import http
from rest_framework import viewsets
from erpq.models import documents
from erpq.api.serializers import documents


class documents(viewsets.ModelViewSet):
    serializer_class = documentsSerializer
    queryset = documents.objects.all().order_by('company')





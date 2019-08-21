from django.conf.urls import url, include
from rest_framework import routers
from testapp.api.views import HydJobsCRUDCBV, PuneJobsCRUDCBV, ChennaiJobsCRUDCBV, BloreJobsCRUDCBV


router = routers.DefaultRouter()
router.register('hydjobsinfo', HydJobsCRUDCBV)
router.register('blorejobsinfo', BloreJobsCRUDCBV)
router.register('punejobsinfo', PuneJobsCRUDCBV)
router.register('chennaijobsinfo', ChennaiJobsCRUDCBV)

urlpatterns = [
    url(r'', include(router.urls)),
]

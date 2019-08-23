from django.conf.urls import url, include
from rest_framework import routers
from erpq.api.view import documents
from django.contrib import admin

router = routers.DefaultRouter()
router.register('documents', documents)

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'', include(router.urls)),
]

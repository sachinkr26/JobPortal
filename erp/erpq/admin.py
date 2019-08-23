from django.contrib import admin
from erpq.models import documents


class documentsAdmin(admin.ModelAdmin):
    list_display = ['first', 'last','birthday','email', 'phonenumber','image']




admin.site.register(documents, documentsAdmin)
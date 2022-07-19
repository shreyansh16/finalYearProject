from django.contrib import admin
from .models import Appointment, Reviews, DocumentUpload
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Reviews)
admin.site.register(DocumentUpload)
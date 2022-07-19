from django.contrib import admin
from .models import Specialization, BannedUser


admin.site.register(Specialization)
admin.site.register(BannedUser)

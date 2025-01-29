from django.contrib import admin
from .models import PatientUser, DoctorUser, BaseUser

admin.site.register(BaseUser)
admin.site.register(PatientUser)
admin.site.register(DoctorUser)

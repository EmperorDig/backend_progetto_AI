from django.contrib import admin
from .models import PatientUser, DoctorUser

admin.site.register(PatientUser)
admin.site.register(DoctorUser)

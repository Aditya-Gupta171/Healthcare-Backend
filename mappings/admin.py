from django.contrib import admin

from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
	list_display = ("id", "patient", "doctor", "assigned_at")
	search_fields = ("patient__full_name", "doctor__full_name")

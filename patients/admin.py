from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ("id", "full_name", "age", "gender", "created_by", "created_at")
	search_fields = ("full_name", "contact_number", "created_by__email")
	list_filter = ("gender", "created_at")

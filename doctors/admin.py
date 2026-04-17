from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
	list_display = ("id", "full_name", "specialization", "email", "years_of_experience", "created_at")
	search_fields = ("full_name", "specialization", "email")
	list_filter = ("specialization", "created_at")

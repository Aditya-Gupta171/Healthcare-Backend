from django.db import models


class Doctor(models.Model):
	full_name = models.CharField(max_length=255)
	specialization = models.CharField(max_length=120)
	email = models.EmailField(unique=True)
	contact_number = models.CharField(max_length=20)
	years_of_experience = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.full_name} ({self.specialization})"

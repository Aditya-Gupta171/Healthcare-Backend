from django.db import models
from django.conf import settings


class Patient(models.Model):
	GENDER_CHOICES = (
		("male", "Male"),
		("female", "Female"),
		("other", "Other"),
	)

	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients")
	full_name = models.CharField(max_length=255)
	age = models.PositiveIntegerField()
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
	contact_number = models.CharField(max_length=20)
	address = models.CharField(max_length=255, blank=True)
	medical_history = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.full_name

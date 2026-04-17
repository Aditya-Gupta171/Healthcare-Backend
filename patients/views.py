from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = PatientSerializer

	def get_queryset(self):
		return Patient.objects.filter(created_by=self.request.user).order_by("-created_at")

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)


class PatientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = PatientSerializer

	def get_queryset(self):
		return Patient.objects.filter(created_by=self.request.user)

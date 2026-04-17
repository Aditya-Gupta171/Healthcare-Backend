from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.serializers import DoctorSerializer
from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class PatientDoctorMappingListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = PatientDoctorMappingSerializer

	def get_queryset(self):
		return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user).select_related(
			"patient", "doctor"
		)


class MappingByPatientOrDeleteAPIView(APIView):
	def get(self, request, pk):
		patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
		mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related("doctor")
		doctors = [mapping.doctor for mapping in mappings]
		doctor_data = DoctorSerializer(doctors, many=True).data
		return Response({"patient_id": patient.id, "doctors": doctor_data}, status=status.HTTP_200_OK)

	def delete(self, request, pk):
		mapping = get_object_or_404(PatientDoctorMapping, pk=pk, patient__created_by=request.user)
		mapping.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

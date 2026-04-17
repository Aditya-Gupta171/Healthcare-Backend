from django.urls import path

from .views import MappingByPatientOrDeleteAPIView, PatientDoctorMappingListCreateAPIView

urlpatterns = [
    path("", PatientDoctorMappingListCreateAPIView.as_view(), name="mapping-list-create"),
    path("<int:pk>/", MappingByPatientOrDeleteAPIView.as_view(), name="mapping-get-or-delete"),
]

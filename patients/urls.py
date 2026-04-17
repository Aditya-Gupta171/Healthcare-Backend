from django.urls import path

from .views import PatientListCreateAPIView, PatientRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", PatientListCreateAPIView.as_view(), name="patient-list-create"),
    path("<int:pk>/", PatientRetrieveUpdateDestroyAPIView.as_view(), name="patient-detail"),
]

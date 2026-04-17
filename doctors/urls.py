from django.urls import path

from .views import DoctorListCreateAPIView, DoctorRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", DoctorListCreateAPIView.as_view(), name="doctor-list-create"),
    path("<int:pk>/", DoctorRetrieveUpdateDestroyAPIView.as_view(), name="doctor-detail"),
]

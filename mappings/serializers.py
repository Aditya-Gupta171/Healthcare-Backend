from rest_framework import serializers

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "assigned_at")
        read_only_fields = ("id", "assigned_at")

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient")

        if request and patient and patient.created_by_id != request.user.id:
            raise serializers.ValidationError("You can only map doctors to your own patients.")

        if PatientDoctorMapping.objects.filter(patient=attrs.get("patient"), doctor=attrs.get("doctor")).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")

        return attrs

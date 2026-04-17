from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id",
            "full_name",
            "specialization",
            "email",
            "contact_number",
            "years_of_experience",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_years_of_experience(self, value):
        if value < 0 or value > 80:
            raise serializers.ValidationError("Years of experience must be between 0 and 80.")
        return value

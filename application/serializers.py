from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.get_full_name', read_only=True)
    tutor_name = serializers.CharField(
        source='tutor.user.get_full_name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'student_name',
            'tutor',
            'tutor_name',
            'status',
            'applied_at',
            'cancel'
        ]

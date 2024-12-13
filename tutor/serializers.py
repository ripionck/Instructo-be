from rest_framework import serializers
from .models import Tutor, Review, SubjectChoice


class SubjectChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectChoice
        fields = '__all__'


class TutorSerializer(serializers.ModelSerializer):
    subjects = SubjectChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Tutor
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

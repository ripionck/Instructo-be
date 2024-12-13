from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student
from core.constrains import GENDER_CHOICES, MEDIUM_OF_INSTRUCTION_CHOICES


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class StudentRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    image = serializers.ImageField(required=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)
    mobile = serializers.CharField(max_length=15, required=True)
    location = serializers.CharField(max_length=100, required=True)
    tuition_district = serializers.CharField(max_length=100, required=True)
    medium_of_instruction = serializers.ChoiceField(
        choices=MEDIUM_OF_INSTRUCTION_CHOICES,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password', 'confirm_password', 'image', 'gender',
            'mobile', 'location', 'tuition_district',
            'medium_of_instruction'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'error': "Passwords don't match"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'error': "Email already exists"})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password')

        # Extract Student model fields
        student_fields = {
            'image': validated_data.pop('image'),
            'gender': validated_data.pop('gender'),
            'mobile': validated_data.pop('mobile'),
            'location': validated_data.pop('location'),
            'tuition_district': validated_data.pop('tuition_district'),
            'medium_of_instruction': validated_data.pop('medium_of_instruction'),
        }

        # Create User instance
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        # Create Student instance
        Student.objects.create(user=user, **student_fields)

        return user


class TutorLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(
        required=True, write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect"})
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "New passwords do not match"})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AdminModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested serializer for user details

    class Meta:
        model = AdminModel
        fields = ['id', 'mobile_no', 'user']


class AdminRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    mobile_no = serializers.CharField(
        max_length=14,
        help_text="Enter number in format: +8801234567890"
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'mobile_no', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_mobile_no(self, value):
        if AdminModel.objects.filter(mobile_no=value).exists():
            raise serializers.ValidationError(
                "This mobile number is already registered")
        return value

    def save(self):
        user_data = {
            'username': self.validated_data['username'],
            'first_name': self.validated_data['first_name'],
            'last_name': self.validated_data['last_name'],
            'email': self.validated_data['email']
        }

        if self.validated_data['password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError(
                {'error': "Passwords don't match"})

        if User.objects.filter(email=user_data['email']).exists():
            raise serializers.ValidationError(
                {'error': "Email already exists"})

        user = User(**user_data)
        user.set_password(self.validated_data['password'])
        user.is_active = False
        user.save()

        AdminModel.objects.create(
            user=user,
            mobile_no=self.validated_data['mobile_no']
        )
        return user


class AdminLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = AdminModel
        fields = ['username', 'password']

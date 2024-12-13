from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Student
from .serializers import (
    StudentSerializer,
    StudentRegistrationSerializer,
    TutorLoginSerializer,
    ChangePasswordSerializer
)
from tutor.models import Tutor
from tutor.serializers import TutorSerializer


class StudentFilterViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:8000/student/active/{
                uid}/{token}"
            email_subject = "Confirm Your Student Registration"
            email_body = render_to_string('confirm_email.html', {
                'confirm_link': confirm_link,
                'user': user
            })

            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[user.email]
            )
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response(
                {"message": "Please check your email to confirm registration"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginApiView(APIView):
    def post(self, request):
        serializer = TutorLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user and hasattr(user, 'student_profile'):
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)

                return Response({
                    'token': token.key,
                    'student_id': user.student_profile.id
                }, status=status.HTTP_200_OK)
            return Response(
                {'error': "Invalid credentials or student profile not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK
        )


class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password updated successfully"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassFilter(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tuition_class']

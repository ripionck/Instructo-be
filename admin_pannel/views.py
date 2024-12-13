from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import AdminModel
from .serializers import (
    AdminSerializer,
    AdminRegistrationSerializer,
    AdminLoginSerializer
)


class AdminApiView(APIView):
    def get(self, request):
        admins = AdminModel.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    serializer_class = AdminRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:8000/adminpannel/active/{
                uid}/{token}"
            email_subject = "Confirm Your Admin Registration"
            email_body = render_to_string('confirm_email.html', {
                'confirm_link': confirm_link
            })

            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[user.email]
            )
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response(
                {"message": "Please check your email for confirmation"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate_view(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return redirect('register')


class AdminLoginApiView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                try:
                    admin = AdminModel.objects.get(user=user)
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request, user)

                    return Response({
                        'token': token.key,
                        'admin_id': admin.id
                    }, status=status.HTTP_200_OK)
                except AdminModel.DoesNotExist:
                    return Response(
                        {'error': "Admin profile not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            return Response(
                {'error': "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLogoutApiView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            logout(request)
            return Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

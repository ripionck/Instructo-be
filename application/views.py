from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationListCreateView(APIView):
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Application, pk=pk)

    def get(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    def put(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        application = self.get_object(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

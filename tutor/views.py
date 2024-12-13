from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import Tutor, Review
from .serializers import TutorSerializer, ReviewSerializer


class TutorViewset(APIView):
    def get(self, request, format=None):
        tutors = Tutor.objects.all()
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewset(APIView):
    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorDetail(APIView):
    def get_object(self, pk):
        try:
            return Tutor.objects.get(pk=pk)
        except Tutor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tutor = self.get_object(pk)
        serializer = TutorSerializer(tutor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tutor = self.get_object(pk)
        serializer = TutorSerializer(tutor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tutor = self.get_object(pk)
        tutor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TutorList(APIView):
    def get(self, request, format=None):
        tutors = Tutor.objects.all()
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Radiologist
from .serializers import RadiologistRegisterSerializer

class RadiologistViewSet(viewsets.ModelViewSet):
    queryset = Radiologist.objects.all()
    serializer_class = RadiologistRegisterSerializer

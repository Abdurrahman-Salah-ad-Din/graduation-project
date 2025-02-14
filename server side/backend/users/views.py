from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Radiologist
from .serializers import RadiologistSerializer

class RadiologistViewSet(viewsets.ModelViewSet):
    queryset = Radiologist.objects.all()
    serializer_class = RadiologistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        radiologists = super().get_queryset()
        if not self.request.user.is_staff:
            radiologists = radiologists.filter(id=self.request.user.id)
        return radiologists
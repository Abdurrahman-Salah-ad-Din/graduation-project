from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Radiologist
from .serializers import RadiologistSerializer, LoginSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class RadiologistViewSet(viewsets.ModelViewSet):
    queryset = Radiologist.objects.all()
    serializer_class = RadiologistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        radiologists = super().get_queryset()
        if not self.request.user.is_staff:
            radiologists = radiologists.filter(id=self.request.user.id)
        return radiologists
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
from .models import PatientScan
from rest_framework import viewsets, permissions
from .serializers import PatientScanSerializer

class PatientScanView(viewsets.ModelViewSet):
    queryset = PatientScan.objects.select_related('patient').prefetch_related('predictions').all()
    serializer_class = PatientScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(patient__radiologists=user).distinct()

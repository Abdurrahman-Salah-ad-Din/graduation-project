from django.db.models import Q
from rest_framework import views, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PatientAccessRequestSerialzier, PatientSerializer
from .models import Patient

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('created_by').prefetch_related(
        'radiologists',
        'scans',
        'scans__predictions',
        'scans__predictions__disease'
    )
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(created_by=user) | Q(radiologists=user)).distinct()

    def get_serializer_class(self):
        if self.action == "grant_access":
            return PatientAccessRequestSerialzier
        return super().get_serializer_class()

    @action(detail=False, methods=["post"], url_path="grant-access",)
    def grant_access(self, request):
        serializer = PatientAccessRequestSerialzier(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Access granted."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
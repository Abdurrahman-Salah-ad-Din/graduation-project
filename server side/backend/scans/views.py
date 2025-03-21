from .models import Disease, OrganChoices, PatientScan, ScanDiseasePrediction
from rest_framework import viewsets, permissions, mixins
from .serializers import PatientScanSerializer
from core.ai.factory import get_ai_model
from django.db import transaction
from django.db.models import Prefetch

class PatientScanView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = PatientScan.objects.select_related('patient').prefetch_related(Prefetch('predictions', queryset=ScanDiseasePrediction.objects.select_related('disease')), 'predictions__disease').all()
    serializer_class = PatientScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(patient__radiologists=user).distinct()

    def perform_create(self, serializer):
        with transaction.atomic():        
            scan = serializer.save()
            predictions_data = get_ai_model(OrganChoices(scan.organ)).predict(scan.image_scan_url.path)
            predicted_disease_names = list(predictions_data.keys())
            existing_diseases = Disease.objects.filter(name__in=predicted_disease_names)
            disease_map = {d.name: d for d in existing_diseases}
            
            predictions_to_create = []
            for disease_name, confidence in predictions_data.items():
                # Create or fetch the Disease object (you might still need a query here)
                disease_obj = disease_map.get(disease_name)
                if not disease_obj:
                    disease_obj = Disease.objects.create(name=str(disease_name))
                    disease_map[disease_name] = disease_obj
                predictions_to_create.append(ScanDiseasePrediction(
                    scan=scan,
                    disease=disease_obj,
                    confidence=confidence
                ))

            ScanDiseasePrediction.objects.bulk_create(predictions_to_create)
        return scan
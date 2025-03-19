from patients.models import PatientRadiologistAccess, Patient
from .models import Disease, PatientScan, ScanDiseasePrediction
from rest_framework import serializers

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['id', 'name']

class ScanDiseasePredictionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer().data.get('name')

    class Meta:
        model = ScanDiseasePrediction
        fields = ('id', 'disease', 'confidence',)
        read_only_fields = ('id',)

class PatientScanSerializer(serializers.ModelSerializer):
    class CurrentUserPatientField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                return Patient.objects.prefetch_related('created_by').filter(
                    id__in=PatientRadiologistAccess.objects.filter(
                        radiologist=request.user
                    ).values('patient')
                )
            return PatientRadiologistAccess.objects.none()

    predictions = ScanDiseasePredictionSerializer(many=True, read_only=True)
    patient = CurrentUserPatientField()

    class Meta:
        model = PatientScan
        fields = ('id', 'patient', 'image_scan_url', 'organ', 'additional_info', 'created_at', 'predictions')
        read_only_fields = ('id', 'created_at', 'predictions')
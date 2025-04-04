from patients.models import PatientRadiologistAccess, Patient
from .models import PatientScan, ScanDiseasePrediction
from rest_framework import serializers
from core.exceptions import AppException
from core.errors import ErrorCodes

class ScanDiseasePredictionSerializer(serializers.ModelSerializer):
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

    def validate_image_scan_url(self, value):
        if not value:
            raise AppException(ErrorCodes.SCAN_002, field="image_scan_url")
        
        if value.size > 10 * 1024 * 1024:
            raise AppException(ErrorCodes.SCAN_005, 
                              "Image too large. Maximum size is 10MB.", 
                              field="image_scan_url")
            
        return value

    class Meta:
        model = PatientScan
        fields = ('id', 'patient', 'image_scan_url', 'organ', 'additional_info', 'created_at', 'predictions')
        read_only_fields = ('id', 'created_at', 'predictions')
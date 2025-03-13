from rest_framework import serializers
from .models import Patient, PatientRadiologistAccess
from users.models import Radiologist

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'code', 'created_by',
        )
        read_only_field = ('id', 'code', 'created_by',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
class PatientAccessRequestSerialzier(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        try:
            patient = Patient.objects.get(code=self.code)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Invalid patient code.")
        self.context['patient'] = patient
        return value
    
    def create(self, validated_data):
        patient = self.context['patient']
        radiologist = self.context['request'].user

        if PatientRadiologistAccess.objects.filter(patient=patient, radiologist=radiologist).exists():
           raise serializers.ValidationError("You already have access to this patient.") 
        
        access = PatientRadiologistAccess.objects.create(patient=patient, radiologist=radiologist)
        return access
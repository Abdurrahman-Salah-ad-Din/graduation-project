from rest_framework import serializers
from .models import Patient, PatientRadiologistAccess
from scans.serializers import PatientScanSerializer

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.

    Includes a nested read-only representation of the patient's scans.
    Automatically sets the 'created_by' field to the logged-in Radiologist.
    """
    scans = PatientScanSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = (
            'id', 'email', 'first_name', 'last_name', 'date_of_birth', 
            'gender', 'code', 'created_by', 'scans',
        )
        read_only_fields = ('id', 'code', 'created_by',)

    def create(self, validated_data):
        """
        Create a Patient record, setting the 'created_by' field to the current user.
        Also creates an access record so that the creator has access to the patient.
        """
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        patient = super().create(validated_data)
        # Automatically grant the creating radiologist access to the patient.
        PatientRadiologistAccess.objects.create(patient=patient, radiologist=request.user)
        return patient
    
class PatientAccessRequestSerialzier(serializers.Serializer):
    """
    Serializer for a Radiologist to request access to a patient using an invitation code.
    """
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        """
        Validate the invitation code and set the corresponding patient in the context.
        """
        try:
            patient = Patient.objects.get(code=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Invalid patient code.")
        self.context['patient'] = patient
        return value
    
    def create(self, validated_data):
        """
        Create an access record in the junction table.
        Raises an error if access already exists.
        """
        patient = self.context['patient']
        radiologist = self.context['request'].user

        if PatientRadiologistAccess.objects.filter(patient=patient, radiologist=radiologist).exists():
           raise serializers.ValidationError("You already have access to this patient.") 
        
        access = PatientRadiologistAccess.objects.create(patient=patient, radiologist=radiologist)
        return access
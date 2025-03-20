from django.db import models
from users.models import Radiologist
from core.utils import get_secret_code
from phonenumber_field.modelfields import PhoneNumberField

class Patient(models.Model):
    """
    Represents a patient in the system.

    Fields:
        email: Unique email for the patient.
        code: A unique 6-digit invitation code generated automatically.
        first_name, last_name: The patient's names.
        date_of_birth: Patient's birth date.
        phone_number: Optional phone number.
        gender: Patient's gender (choices provided by GenderChoices).
        created_at: The date-time when the patient is created.
        created_by: The Radiologist (doctor) who created this patient record.
        radiologists: Many-to-many relationship with Radiologist through a junction table.
    """
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    def generate_random_code():
        """
        Generate a random 6-digit code using get_secret_code utility.
        """
        return get_secret_code(6)
    
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, default=generate_random_code)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=1, choices=GenderChoices)
    # The Radiologist who created the patient record.
    created_by = models.ForeignKey(Radiologist, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_patients")
    # Many-to-many: additional Radiologists with access to this patient.
    radiologists = models.ManyToManyField(Radiologist, through='PatientRadiologistAccess', related_name='accessible_patients')

    def __str__(self):
        # Returns a string representation including the patient name, code, and creator.
        return f"{self.first_name} {self.last_name} diagnosed by {self.created_by}"
    
class PatientRadiologistAccess(models.Model):
    """
    Junction table that links a Patient with a Radiologist who has been granted access.

    Fields:
        radiologist: The Radiologist (doctor or nurse) who gains access.
        patient: The patient record to which access is granted.
        granted_at: Timestamp when access was granted.
    """
    radiologist = models.ForeignKey(Radiologist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'radiologist')
        indexes = [
            models.Index(fields=['patient', 'radiologist'])
        ]
    
    def __str__(self):
        # Returns a string representation of the access record.
        return f"Access for {self.radiologist.get_full_name()} to patient {self.patient.first_name} {self.patient.last_name} granted at {self.granted_at}"
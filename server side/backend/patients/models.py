from tkinter import CASCADE
import uuid
from django.utils import timezone
from django.db import models
from users.models import Radiologist
from core.utils import get_secret_code

class Patient(models.Model):
    class GenderChoices:
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    def generate_random_code():
        return get_secret_code(6)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GenderChoices)
    code = models.CharField(max_length=6, default=generate_random_code)
    created_by = models.ForeignKey(Radiologist, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_patients")
    radiologists = models.ManyToManyField(Radiologist, through='PatientRadiologistAccess', related_name='accessible_patients')

    def _str_(self):
        return f"{self.first_name} {self.last_name} diagnosed by {self.diagnosed_by}"
    
class PatientRadiologistAccess(models.Model):
    radiologist = models.ForeignKey(Radiologist, on_delete=CASCADE)
    patient = models.ForeignKey(Patient, on_delete=CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'radiologist')
    
    def __str__(self):
        return f"Access for {self.radiologist.get_full_name()} to patient {self.patient.first_name} {self.patient.last_name} granted at {self.granted_at}"
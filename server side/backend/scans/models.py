from django.db import models
from patients.models import Patient

class OrganChoices(models.TextChoices):
        HEART = 'H', 'Heart'
        BRAIN = 'B', 'Brain'
        CHEST = 'C', 'Chest'

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class PatientScan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name='scans', null=True)
    image_scan_url = models.ImageField(upload_to='patient_scans/')
    organ = models.CharField(max_length=1, choices=OrganChoices)
    additional_info = models.CharField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan {self.id} for {self.patient.first_name} {self.patient.last_name} ({self.organ})."
    
class ScanDiseasePrediction(models.Model):
    scan = models.ForeignKey(PatientScan, on_delete=models.CASCADE, related_name="predictions")
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, max_length=255)
    confidence = models.FloatField()

    class Meta:
        unique_together = ('scan', 'disease')

    def __str__(self):
        return f"{self.disease.name} ({self.confidence*100:.1f}%) for Scan {self.scan.id}"
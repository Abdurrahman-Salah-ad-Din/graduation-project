import uuid
from django.utils import timezone
from django.db import models
from users.models import Radiologist

class Patient(models.Model):
    class GenderChoices:
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GenderChoices)
    diagnosis_date = models.DateField(default=timezone.now)
    diagnosed_by = models.ForeignKey(Radiologist, on_delete=models.SET_NULL, related_name='diagnosed_patients')

    def _str_(self):
        return f"{self.first_name} {self.last_name} diagnosed by {self.diagnosed_by}"
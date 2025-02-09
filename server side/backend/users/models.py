from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class RadiologistManager(UserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Radiologist(AbstractUser):
    class JobChoices(models.TextChoices):
        DOCTOR = 'D', 'Doctor'
        NURSE = 'N', 'Nurse'

    class GenderChoices(models.TextChoices):
        male = 'M', 'Male'
        Female = 'F', 'Female'

    date_of_birth = models.DateField(null=True, blank=True)
    job = models.CharField(max_length=1,choices=JobChoices)
    gender = models.CharField(max_length=1, choices=GenderChoices)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'job', 'gender')

    objects = RadiologistManager()

    def __str__(self):
        return f"{self.get_full_name()}"
    
    def has_perm(self, perm, obj = None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return True
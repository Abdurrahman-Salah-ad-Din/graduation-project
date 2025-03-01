from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField

class RadiologistManager(UserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class Radiologist(AbstractUser):
    class JobChoices(models.TextChoices):
        DOCTOR = 'D', 'Doctor'
        NURSE = 'N', 'Nurse'

    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    date_of_birth = models.DateField()
    job = models.CharField(max_length=1,choices=JobChoices.choices)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'job', 'gender', 'phone_number', 'date_of_birth']

    objects = RadiologistManager()

    def __str__(self):
        return f"{self.get_full_name()}"
    
class PasswordResetOTP(models.Model):
    EXPIRATION_MINUTES = 15

    user = models.ForeignKey(Radiologist, on_delete=models.CASCADE, related_name='reset_otps')
    otp = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=self.EXPIRATION_MINUTES)
        return timezone.now() > expiration_time
    
    def __str__(self):
        return f"OTP for {self.user.email} is {self.otp}, created at {self.created_at} and it is {'used' if self.is_used else 'not used'}."
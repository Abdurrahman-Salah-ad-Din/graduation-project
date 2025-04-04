from core.utils import get_secret_code
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Radiologist, PasswordResetOTP
from core.exceptions import AppException
from core.errors import ErrorCodes

class RadiologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radiologist
        fields = (
            'id',
            'email', 
            'first_name', 
            'last_name', 
            'password',
            'phone_number', 
            'gender', 
            'job', 
            'is_staff', 
            'is_active', 
            'date_of_birth',
            'is_superuser'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def create(self, validated_data):
        radiologist = Radiologist.objects.create_user(
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **{k: v for k, v in validated_data.items() if k != 'password'},
        )
        return radiologist

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        if self.__is_admin():
            [setattr(fields[attribute], 'read_only', False) for attribute in ['is_staff', 'is_active', 'is_superuser', 'email'] if attribute in fields]
        return fields
    
    def __is_admin(self):
        request = self.context.get('request')
        return request and request.user and request.user.is_staff


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attr):
        if not attr.get('email'):
            raise AppException(ErrorCodes.USER_001, field="email")
        if not attr.get('password'):
            raise AppException(ErrorCodes.USER_004, field="password")
            
        try:
            data = super().validate(attr)
            
            data.update({
                'radiologist': RadiologistSerializer(self.user).data
            })
            return data
        except Exception as e:
            if "no active account" in str(e).lower():
                raise AppException(ErrorCodes.AUTH_001, status_code=401)
        raise
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not value:
            raise AppException(ErrorCodes.USER_001, field="email")
        
        try:
            self.user = Radiologist.objects.get(email=value)
        except Radiologist.DoesNotExist:
            raise AppException(ErrorCodes.USER_014, field="email")
        return value
    
    def save(self):
        otp_value = get_secret_code()
        reset_record = PasswordResetOTP.objects.create(user = self.user,otp = otp_value)

        subject = "OTP to reset you account password"
        message = (
            f"To reset your password, enter this OTP when prompted: {otp_value}\n"
            "It will expire in 15 minutes. Do not share this OTP with anyone."
        )
        from_mail = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]
        send_mail(subject, message, from_mail, recipient_list)

        return reset_record

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=8)

    def validate_email(self, email):
        if not email:
            raise AppException(ErrorCodes.USER_001, field="email")
        return email
    
    def validate_otp(self, otp):
        if not otp:
            raise AppException(ErrorCodes.AUTH_006, field="otp")
        return otp

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        try:
            user = Radiologist.objects.get(email=email)
        except Radiologist.DoesNotExist:
            raise AppException(ErrorCodes.USER_014, field="email")

        try:
            reset_record = user.reset_otps.filter(is_used=False).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            raise AppException(ErrorCodes.AUTH_007, 
                              "No active OTP found. Please request a new one.")

        if reset_record.otp != otp:
            raise AppException(ErrorCodes.AUTH_006, field="otp")
        
        if reset_record.is_expired():
            raise AppException(ErrorCodes.AUTH_004, field="otp")

        attrs['user'] = user
        attrs['reset_record'] = reset_record

        return attrs
    
    def save(self):
        reset_record = self.validated_data['reset_record']
        reset_record.is_verified = True
        reset_record.save()
        return reset_record

class PasswordUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if not email:
            raise AppException(ErrorCodes.USER_001, field="email")
        return email
    
    def validate_new_password(self, new_password):
        if not new_password:
            raise AppException(ErrorCodes.USER_004, field="new_password")
        if len(new_password) < 8:
            raise AppException(ErrorCodes.USER_015, field="new_password")
        return new_password

    def validate_new_password(self, confirm_password):
        if not confirm_password:
            raise AppException(ErrorCodes.USER_004, field="confirm_password")
        return confirm_password

    def validate(self, attrs):
        email = attrs.get('email')

        if attrs['new_password'] != attrs['confirm_password']:
            raise AppException(ErrorCodes.USER_015, 
                              "Passwords do not match", field="confirm_password")

        try:
            user = Radiologist.objects.get(email=email)
        except Radiologist.DoesNotExist:
            raise AppException(ErrorCodes.USER_014, field="email")

        try:
            reset_record = user.reset_otps.filter(is_used=False, is_verified=True).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            raise AppException(ErrorCodes.AUTH_007, 
                              "No verified OTP found. Please verify your OTP first.")
        
        if reset_record.is_expired():
            raise AppException(ErrorCodes.AUTH_004)

        attrs['user'] = user
        attrs['reset_record'] = reset_record

        return attrs

    def save(self):
        self.user.reset_otps.filter(is_used=False).update(is_used=True)

        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        reset_record = self.validated_data['reset_record']

        user.set_password(new_password)
        user.save()

        reset_record.is_used = True
        reset_record.save()

        return user
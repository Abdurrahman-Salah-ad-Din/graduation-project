from rest_framework import serializers
from .models import Radiologist

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
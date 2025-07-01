from rest_framework import serializers
from . models import *
import random
from django.core.mail import send_mail
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        otp = str(random.randint(100000, 999999))
        print(f"OTP : {otp}")
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                otp=otp,
                is_active=False
            )
            send_mail('Your OTP for Account Verification',f'Your OTP is: {otp}',from_email='aromalvv005@gmail.com', recipient_list=[user.email],fail_silently=False,)
        return user
        
class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        user = CustomUser.objects.filter(email=email, otp=otp).first()

        if not user:
            raise Exception("User with this OTP and Email does not exist")
        user.is_active = True
        user.is_verified = True
        user.otp = None
        user.save()
        return data
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    
import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import serializers

from root.settings import EMAIL_HOST_USER
from users.models import User, getKey, setKey


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("full_name", "email", "username", "password")

    def validate(self, attrs):
        activate_code = random.randint(100000, 999999)
        user = User(
            full_name=attrs['full_name'],
            email=attrs['email'],
            username=attrs['username'],
            password=make_password(attrs['password']),
            is_active=True,
        )
        setKey(
            key=attrs['email'],
            value={
                "user": user,
                "activate_code": activate_code
            },
            timeout=300
        )
        print(getKey(key=attrs['email']))
        send_mail(
            subject="Subject here",
            message=f"Your activate code.\n{activate_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[attrs['email']],
            fail_silently=False,
        )
        return super().validate(attrs)


class CheckActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            return attrs
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', "full_name"]

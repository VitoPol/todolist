from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    password_repeat = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate_password_repeat(self, value):
        if value != self.initial_data["password"]:
            raise ValidationError("You entered two different passwords. Please try again.")
        return value

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")
        read_only_fields = ("id",)


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ("old_password", "new_password")

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError("Incorrect password")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance

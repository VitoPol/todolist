from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password_repeat"]

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

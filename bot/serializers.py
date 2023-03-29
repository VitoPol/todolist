from rest_framework import serializers

from bot.models import TgUser


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = "__all__"
        read_only_fields = ("tg_chat_id", "tg_user_id", "user")

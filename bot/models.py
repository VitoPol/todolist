from django.db import models

from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.PositiveIntegerField()
    tg_user_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    verification_code = models.CharField(max_length=30, null=True)

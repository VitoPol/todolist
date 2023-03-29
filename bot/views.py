from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import VerifySerializer
from bot.tg.client import TgClient
from todolist.settings import BOT_TOKEN


class VerifyView(UpdateAPIView):
    queryset = TgUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VerifySerializer

    # def get_queryset(self):
    #     code = self.request.data["verification_code"]
    #     return TgUser.objects.filter(verification_code=code)

    def get_object(self):
        code = self.request.data["verification_code"]
        return get_object_or_404(self.queryset, verification_code=code)

    def patch(self, request, *args, **kwargs):
        tg_client = TgClient(BOT_TOKEN)
        instance = self.get_object()
        instance.user = self.request.user
        instance.save()
        tg_client.send_message(instance.tg_chat_id, f"Верификация прошла успешно")
        return Response(self.serializer_class.data)

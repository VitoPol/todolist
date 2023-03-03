from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from core.models import User
from core.serializers import SignUpSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"username": username, "password": password})
        else:
            raise AuthenticationFailed("Неверное имя пользователя или пароль")

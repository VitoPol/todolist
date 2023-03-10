from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, get_object_or_404, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import SignUpSerializer, UserSerializer, PasswordUpdateSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"username": username, "password": password})
        else:
            raise AuthenticationFailed("Неверное имя пользователя или пароль")


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.request.user.id)

    # @method_decorator(ensure_csrf_cookie)
    # def put(self, request, *args, **kwargs):
    #     return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()


class PasswordUpdateView(UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.request.user.id)

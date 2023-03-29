from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from bot import views

urlpatterns = [
    path('verify', views.VerifyView.as_view()),
]

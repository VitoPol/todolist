from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from core import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', LogoutView.as_view(), name='logout'),

    path("signup", views.SignUpView.as_view())
]

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from core import views

urlpatterns = [
    path('signup', views.SignUpView.as_view()),
    path('login', views.LoginView.as_view()),

    path('profile', views.ProfileView.as_view()),
    path('update_password', views.PasswordUpdateView.as_view()),
]

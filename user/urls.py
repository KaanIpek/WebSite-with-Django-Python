from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView, LoginView

app_name="user"

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout/',views.logoutUser,name="logout"),
    
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
  
]
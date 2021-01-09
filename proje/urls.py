"""proje URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from job import views
from django_email_verification import urls as mail_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('admin/', admin.site.urls),
     path('email',include(mail_urls)),
     path('',views.index,name="index"),
     path('about/',views.about,name="about"),
     path('help/',views.help,name="help"),
     path('contact/',views.contact,name="contact"),
     path('contracted/',views.contracted,name="contracted"),
     path('contracted2/',views.contracted2,name="contracted2"),
     path('contractedhelp/',views.contractedhelp,name="contractedhelp"),
     path('user/',include("user.urls")),
     path('mailbody/',include(mail_urls),name="mailbody"),
     path('jobs/',include("job.urls")),
     path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
     path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
     path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
     
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User as user
from django.contrib.auth import login,authenticate,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
# Create your views here.




class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Hatalı Email Adresi'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Bu Email Adresi Kullanımda,Lütfen Başka Bir Email Adresi Seçiniz'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Kullanıcı Adı Sadece Karakterlerden Oluşabilir'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Bu Kullanıcı Adı Kullanımda,Lütfen Başka Bir Kulllanıcı Adı Seçiniz'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account
    
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('user:activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Hesabınızı Aktifleştirin'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Merhaba '+user.username + ', Hesabınızı Aktifleştirmek İçin Linke Tıklayınız \n'+activate_url,
                    'unhelp20@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Hesap Başarıyla Oluşturuldu,Lütfen Aktifleştirmek İçin Email Adresinizi Kontrol Ediniz')
                return render(request, 'register.html')

        return render(request, 'register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'Hesap Zaten Aktif')

            if user.is_active:
                return redirect('user:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Hesap Başarıyla Aktifleştirildi')
            return redirect('user:login')

        except Exception as ex:
            pass

        return redirect('user:login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Hoşgeldiniz, ' +
                                     user.username+' Giriş Yaptınız')
                    return redirect('index')
                messages.error(
                    request, 'Hesabınız Aktifleştirilmemiş,Email Adresinizi Kontrol Ediniz')
                return render(request, 'login.html')
            messages.error(
                request, 'Kullanıcı Adı veya Şifre Hatalı')
            return render(request, 'login.html')

        messages.error(
            request, 'Lütfen Tüm alanları doldurunuz')
        return render(request, 'login.html')
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış yaptınız")
    return redirect("index")
"""class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('index')"""

        
"""def mailbody(request):
    form= RegisterForm(request.POST or None)
    if form.is_valid():
        username =form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = get_user_model().objects.create(username=username, password=password, email=email)
        sendConfirm(user)
    return redirect("index")
def register(request):
    form= RegisterForm(request.POST or None)
    if form.is_valid():
        username =form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')   
        new_user = form.save(commit=False)
        new_user.set_password(password)
        new_user.save()
        send_mail("Kayıt Olduğunuz İçin Teşekkür Ederiz...","Tüm işlerin kolaylıkla yapıldığı dünyamıza hoş geldiniz...",settings.EMAIL_HOST_USER,[new_user.email, settings.EMAIL_HOST_USER],fail_silently=True)
        user = authenticate(username =username,password =password)
        login(request,user)
        messages.success(request,"Başarıyla Kayıt Oldunuz...")
        return redirect("index")
    context= {

        "form": form
    }
    return render(request,"register.html",context)
   
def loginUser(request):
    form = LoginForm(request.POST or None)
    
    context = {
        "form" : form
    }
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user = authenticate(request,username = username,password = password)


        if user is None:
            messages.info(request,"Kullanıcı adı veya Parola Hatalı")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla Giriş yaptınız")  
        login(request,user)
        return redirect("index")  
    return render(request,"login.html",context)

"""


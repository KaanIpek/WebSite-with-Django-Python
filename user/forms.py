from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget = forms.PasswordInput)
    
class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=50,label="kullanıcı adı")
    email = forms.EmailField(max_length=50,label="Email")
    password = forms.CharField(max_length=20,label="Parola",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parolayı Doğrula",widget=forms.PasswordInput)
    class Meta:
        model=User 
        fields =['username','email','password','confirm']
        
    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        values = {

            "username" : username,
            "email" :email,
            "password" : password
        }
        return values
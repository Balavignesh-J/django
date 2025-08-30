from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Contact(forms.Form):
    name=forms.CharField(max_length=100,label='name')
    email=forms.EmailField(max_length=100,label='email')
    message=forms.CharField(max_length=300,label='message')

class Register(forms.ModelForm):
    username=forms.CharField(label='username' ,max_length=200 ,required=True)
    email=forms.CharField(label='email' ,max_length=200 ,required=True)
    password=forms.CharField(label='password' ,max_length=200 ,required=True)
    password_confirm=forms.CharField(label='password_confirm' ,max_length=200 ,required=True)

    class Meta:
        model=User
        fields=['username','email','password']
    
    def clean(self):
        data = super().clean()
        password=data.get('password')
        password_confirm=data.get('password_confirm')
        
        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
class Login(forms.Form):
    username=forms.CharField(label='username' ,max_length=100 ,required=True)
    password=forms.CharField(label='password' ,max_length=100 ,required=True)

    def clean(self):
        data = super().clean()
        username=data.get('username')
        password=data.get('password')

        if username and password:
            user = authenticate(username=username , password=password)
            if user is None:
                raise forms.ValidationError("user doesn't exist please register")
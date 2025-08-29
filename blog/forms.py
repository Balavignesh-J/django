from django import forms
from django.contrib.auth.models import User

class Contact(forms.Form):
    name=forms.CharField(max_length=100,label='name')
    email=forms.EmailField(max_length=100,label='email')
    message=forms.CharField(max_length=300,label='message')

class Register(forms.ModelForm):
    username=forms.CharField(label='username' ,max_length=200)
    email=forms.CharField(label='email' ,max_length=200)
    password=forms.CharField(label='password' ,max_length=200)
    password_confirm=forms.CharField(label='password_confirm' ,max_length=200)

    class Meta:
        model=User
        fields=['username','email','password']
    
    def clean(self):
        data = super().clean()
        password=data.get('password')
        password_confirm=data.get('password_confirm')
        
        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError('Passwords do not match')
    
from django import forms

class contact(forms.Form):
    name=forms.CharField(max_length=100,label='name')
    email=forms.EmailField(max_length=100,label='email')
    message=forms.CharField(max_length=300,label='message')
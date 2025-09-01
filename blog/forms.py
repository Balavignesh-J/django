from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Category, Detail

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
            
class Forgot_password(forms.Form):
    email = forms.EmailField(label="Email", required=True)  # Make email required

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist")
        return email

class Resetpassword(forms.Form):
    new_password = forms.CharField(label="new_password", max_length=200, required=True)
    confirm_password = forms.CharField(label="confirm_password", max_length=200, required=True)

    def clean(self):
        data = super().clean()
        newpassword=data.get('new_password')
        confirmpassword=data.get('confirm_password')
        
        if newpassword and confirmpassword and newpassword!=confirmpassword:
            raise forms.ValidationError('Passwords do not match')
        
class New_post(forms.ModelForm):
    title = forms.CharField(label="title", max_length=200, required=True)
    content = forms.CharField(label="content", max_length=1000, required=True)
    category = forms.ModelChoiceField(label="category", required=True, queryset=Category.objects.all())
    img_url = forms.ImageField(label="img_url", required=False)

    class Meta:
        model = Detail
        fields=["title","content","category","img_url"]

    def clean(self):
        data = super().clean()
        title = data.get("title")
        content = data.get("content")

        if title and len(title)<5:
            raise forms.ValidationError("Title requires minimum 5 characters")
        if content and len(content)<10:
            raise forms.ValidationError("Content requires minimum 10 characters")
        
    def save(self, commit=...):
        post=super().save(commit)
        img_url = self.cleaned_data.get("img_url")    
        if img_url:
            post.img_url = img_url
        else:
            post.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/250px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        
        if commit:
            post.save()
        return post
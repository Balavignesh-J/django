from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category, Detail,About
from blog.forms import Contact, New_post,Register,Login,Forgot_password, Resetpassword
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

import logging
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group

def index(request):
    detail=Detail.objects.all()
    page=Paginator(detail,5)
    pg_no=request.GET.get('page')
    pg_obj=page.get_page(pg_no)

    home='Page'
    return render(request,'blog/index.html',{'home':home,'detail':pg_obj})

def detail(request,slug):
    if request.user and not request.user.has_perm("blog.view_detail"):
        messages.error(request, "you are not allowed to view post")
        return redirect("blog:index")
    det=Detail.objects.get(slug=slug)
    relation=Detail.objects.filter(category=det.category).exclude(pk=det.pk)
    return render(request,'blog/detail.html',{'post':det,'related':relation})

def old_url(request):
    return redirect(reverse('blog:new_pg_url'))

def new_url(request):
    return HttpResponse("New views")

def contact_view(request):
        if request.method=='POST':
            form = Contact(request.POST)
            name=request.POST.get('name')
            email=request.POST.get('email')
            message=request.POST.get('message')
            logger = logging.getLogger("TESTING")
            if form.is_valid():
               logger.debug(f"{form.cleaned_data['name']} and {form.cleaned_data['email']} and {form.cleaned_data['message']}")
               success_msg='message sent successfully'
               return render(request,'blog/contact.html',{'form':form,'success_msg':success_msg})
            else:
               logger.debug(f"form validation failure")
            return render(request,'blog/contact.html',{'form':form,'name':name,'email':email,'message':message})
        return render(request,'blog/contact.html')

def about_view(request):
    about=About.objects.get(pk=1)
    return render(request,'blog/about.html',{"about":about})

def register(request):
    form=Register()
    logger = logging.getLogger("TESTING")
    if request.method=='POST':
        form=Register(request.POST) 
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            #group
            reader ,created = Group.objects.get_or_create(name='Readers')
            user.groups.add(reader)
            messages.success(request,'register successful')
            logger.debug(f"{form.cleaned_data['username']} and {form.cleaned_data['email']} and {form.cleaned_data['password']}")
            return redirect('blog:login')
        else:
            logger.debug(f"form validation failure")
        return render(request,'blog/register.html',{'form':form,'name':username,'email':email,'password':password})
    return render(request,'blog/register.html',{'form':form})

def login(request):
    form=Login()
    if request.method=='POST':
        form=Login(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username ,password=password)
            if user is not None:
                auth_login(request ,user)
                return redirect('/dashboard')
    return render(request,'blog/login.html' ,{'form':form})

def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
    all_post = Detail.objects.filter(user=request.user)
    return render(request ,'blog/dashboard.html',{'name':username,"detail":all_post})

def logout_view(request):
    logout(request)
    return redirect(reverse('blog:index'))

def forgot_password(request):
    if request.method=='POST':
        form = Forgot_password(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            site = get_current_site(request)
            domain = site.domain
            subject = 'password reset email'
            message = render_to_string(
                "blog/reset_password_email.html",
                {
                    "domain": domain,
                    "uidb64": uidb64,
                    "token": token,
                    "user": user
                }
            )
            send_mail(subject,message,'noreply@bvcode.com',[email])
            messages.success(request, "email sent successfully")
    else:
        form = Forgot_password()

    return render(request ,"blog/forgot_password.html",{"form":form})

def reset_password(request, uidb64, token):
    form=Resetpassword()
    if request.method=="POST":
        form = Resetpassword(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            try:
                uid= urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None

            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Password reset successful")
                return redirect("blog:login")
            else:
                messages.error(request,"Password reset link expired")
            
    return render(request, "blog/reset_password.html",{"form":form})

@login_required
@permission_required("blog.add_detail", raise_exception=True)
def new_post(request):
    category = Category.objects.all()
    form = New_post()
    if request.method == "POST":
        form = New_post(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect("blog:dashboard")
    return render(request, 'blog/new_post.html',{"category":category,"form":form})

@login_required
def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Detail , id=post_id)
    form = New_post()
    if request.method == "POST":
        form = New_post(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post update successful")
            return redirect("blog:dashboard")
    return render(request, "blog/edit_post.html", {"categories":categories, "post":post,"form":form})
@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Detail , id=post_id)
    post.delete()
    messages.success(request, "Post deleted sucessfully")
    return redirect("blog:dashboard")
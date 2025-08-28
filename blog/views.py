from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Detail,About
from django.core.paginator import Paginator
from blog.forms import contact
import logging

def index(request):
    detail=Detail.objects.all()
    page=Paginator(detail,5)
    pg_no=request.GET.get('page')
    pg_obj=page.get_page(pg_no)

    home='Page'
    return render(request,'blog/index.html',{'home':home,'detail':pg_obj})

def detail(request,slug):
    det=Detail.objects.get(slug=slug)
    relation=Detail.objects.filter(category=det.category).exclude(pk=det.pk)
    return render(request,'blog/detail.html',{'post':det,'related':relation})

def old_url(request):
    return redirect(reverse('blog:new_pg_url'))

def new_url(request):
    return HttpResponse("New views")

def contact_view(request):
        if request.method=='POST':
            form = contact(request.POST)
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
    about=About.objects.get(id=1)
    return render(request,'blog/about.html',{"about":about})
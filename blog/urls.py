from django.urls import path
from . import views
    
app_name = "blog"
urlpatterns = [
    path("", views.index, name='index'),
    path("contact",views.contact_view,name='contact'),
    path("register",views.register,name='register'),
    path("login",views.login,name='login'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("logout",views.logout_view,name='logout'),
    path("forgot_password",views.forgot_password,name='forgot_password'),
    path("reset_password/<uidb64>/<token>/", views.reset_password, name='reset_password'),
    path("about",views.about_view,name='about'),
    path("new_url",views.new_url,name='new_pg_url'),
    path("old_url",views.old_url,name='old_url'),
    path("<slug:slug>",views.detail,name='detail')
]
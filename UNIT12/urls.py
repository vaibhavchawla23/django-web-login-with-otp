"""UNIT12 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url #, include
from django.contrib.auth import views as auth_views
from django.urls import path
from ASMIS.views import profile_view, verify_view #, auth_view ,home_view

urlpatterns = [
    path('verify/',verify_view, name="verify_view"),
    path( '',auth_views.LoginView.as_view(redirect_authenticated_user=True,template_name="auth.html"), name="login"),    
    url('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('profile/', profile_view, name="profile")
]

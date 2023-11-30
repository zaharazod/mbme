"""
URL configuration for mbme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from .views import blog, stylesheet, default, script, login

app_name = 'mbme'
local_urls = ([
    path('css/<str:template_name>.css', stylesheet, name='stylesheet'),
    path('js/<str:template_name>.js', script, name='script'),
    path('<str:slug>/', blog, name='blog'),
    path('', default, name='index'),
], app_name)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('overwatch/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('words/', include('apps.blog.blog_v1.urls', namespace='blog_v1')),
    path('bio/', include('apps.biology.urls', namespace='biology')),
    path('photo/', include('photologue.urls', namespace='photologue')),
    path('', include(local_urls, namespace=app_name)),
]

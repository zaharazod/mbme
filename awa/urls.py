from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import (
    blog, stylesheet, default, 
    script, login, profile, logout,
)
from ..config.config import settings

app_name = settings.get('app_name', 'awa')
local_urls = ([
    path('css/<str:template_name>.css', stylesheet, name='stylesheet'),
    path('js/<str:template_name>.js', script, name='script'),
    path('<str:slug>/', blog, name='blog'),
    path('', default, name='index'),
], app_name)

auth_app_name = 'auth'
auth_urls = ([
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
], 'auth')

admin_url = settings.get('admin_url', '/admin')
urlpatterns = [
    path(f'{admin_url}/', admin.site.urls),
    path('words/', include('apps.blog.blog_v1.urls', namespace='awa.blog')),
    path('auth/social/', include('social_django.urls', namespace='awa.social')),
    path('auth/', include(auth_urls, namespace='awa.auth')),
    path('', include(local_urls, namespace='awa.files')),
]

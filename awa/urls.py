from importlib import import_module
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import (
    blog, stylesheet, default,
    script, login, profile, logout,
)
from awa.settings import config, storage_classes
from re import match

AWA_PATHS = [
    'admin',
    'blog',
    'auth',
]

storage_urls = []
for s, v in storage_classes:
    if isinstance(v, str) and match(r'^[a-z][a-z\.]*[a-z]$', v):
        module_parts = v.split('.')
        func_name = module_parts.pop()
        module_name = '.'.join(module_parts)
        m = import_module(module_name)
        f = getattr(m, func_name, None)
        if callable(f):
            p = path(config.storage[s].url, f, name=s)
            storage_urls.append(p)

app_name = config.get('app_name', 'awa.app')
local_urls = (storage_urls + [
    path('css/<str:template_name>.css', stylesheet, name='stylesheet'),
    path('js/<str:template_name>.js', script, name='script'),
    # path('<str:slug>/', blog, name='blog'),
    path('', default, name='index')
], app_name)

auth_urls = ([
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
], 'auth')

config.setdefault('paths', {})
for url_path in AWA_PATHS:
    config.paths.setdefault(url_path, url_path)

admin_url = config.paths.admin or 'admin'
blog_url = config.paths.blog or 'blog'
auth_url = config.paths.auth or 'auth'

urlpatterns = [
    path(f'{admin_url}/', admin.site.urls),
    path(f'{blog_url}/', include('apps.blog.blog_v1.urls', namespace='awa.blog')),
    path(f'{auth_url}/social/',
         include('social_django.urls', namespace='awa.social')),
    path(f'{auth_url}/', include(auth_urls, namespace='awa.auth')),
    path('', include(local_urls, namespace='awa')),
]

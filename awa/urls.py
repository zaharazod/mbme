from importlib import import_module
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import (
    blog, stylesheet, default,
    script, login, profile, logout,
)
from apps.pages.views import view_page
from awa.settings import config
from django.conf.urls.static import static
from re import match
from .views import index_page

AWA_PATHS = [
    # global
    'admin',
    'auth',
    # # per-user
    # 'blog',
    # 'profile',
]

app_name = 'awa'

config.setdefault('paths', {})
for url_path in AWA_PATHS:
    config.paths.setdefault(url_path, url_path)

storage_urls = []
list(map(storage_urls.extend, [
    static(v.url, document_root=v.root)
    for _, v in config.storage.items()
    if isinstance(v, dict) and v.type == 'local'
]))

# user_urls = ([
#     path(f'{config.paths.blog}/',
#         include('apps.blog.urls', namespace='awa.blog')),
#     # path(f'{config.paths.profile}/', ...)
# ])

local_urls = (storage_urls + [
    # path('', include(user_urls), kwargs={
    #     'username': config.default_username or None})
    # path('<str:slug>/', blog, name='blog'),
], app_name)

auth_urls = ([
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
], 'auth')


urlpatterns = [
    path(f'{config.paths.admin}/', admin.site.urls),
    # path(f'{config.paths.blog}/',
    #     include('apps.blog.urls', namespace='awa.blog')),
    path(f'{config.paths.auth}/social/',
        include('social_django.urls', namespace='awa.social')),
    path(f'{config.paths.auth}/',
        include(auth_urls, namespace='awa.auth')),
    # path(r'~<str:username>/', include(user_urls)),
    path('css/<str:template_name>.css', stylesheet, name='stylesheet'),
    path('js/<str:template_name>.js', script, name='script'),
    path('', include(local_urls)),
    path('<path:path>', view_page),
    path('', index_page),
]


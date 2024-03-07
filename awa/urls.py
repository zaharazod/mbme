# from importlib import import_module
from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
# from apps.mana.views import user_index
# from apps.pages.views import view_page
from awa.settings import config
from django.conf.urls.static import static
# from re import match
from .views import (
    view_context,
    view_user,
    stylesheet,
    script,
    login,
    logout,
)

app_name = "awa"

AWA_PATHS = [
    # global
    "admin",
    "auth",
    # # per-user
    # 'blog',
    # 'profile',
]

config.setdefault("paths", {})
for url_path in AWA_PATHS:
    config.paths.setdefault(url_path, url_path)

config.paths.setdefault("user", "~<slug:username>")

storage_urls = []
list(
    map(
        storage_urls.extend,
        [
            static(v.url, document_root=v.root)
            for _, v in config.storage.items()
            if isinstance(v, dict) and v["type"] == "local"
        ],
    )
)

# user_urls = ([
#     path(f'{config.paths.blog}/',
#         include('apps.blog.urls', namespace='awa.blog')),
#     # path(f'{config.paths.profile}/', ...)
# ])

local_urls = (
    storage_urls
    + [
        path("css/<str:template_name>.css", stylesheet, name="stylesheet"),
        path("js/<str:template_name>.js", script, name="script"),
        # path('', include(user_urls), kwargs={
        #     'username': config.default_username or None})
        # path('<str:slug>/', blog, name='blog'),
    ],
    app_name,
)

auth_urls = (
    [
        path("login/", login, name="login"),
        path("logout/", logout, name="logout"),
    ],
    "auth",
)
user_model = get_user_model()
anchor_urls = (
    [
        path(f"{config.paths.user}/<path:path>", view_user),
        path(f"{config.paths.user}/", view_user),
        path("<path:path>", view_context),
        path("", view_context, {"path": None}),
    ],
    app_name,
)

urlpatterns = [
    path(f"{config.paths.admin}/", admin.site.urls),
    # path(f'{config.paths.blog}/',
    #     include('apps.blog.urls', namespace='awa.blog')),
    path(
        f"{config.paths.auth}/social/",
        include("social_django.urls", namespace="awa.social"),
    ),
    path(f"{config.paths.auth}/", include(auth_urls, namespace="awa.auth")),
    # path(r'~<str:username>/', include(user_urls)),
    path("", include(local_urls)),
    path("", include(anchor_urls)),
    path("", view_context, {"path": None}),
]

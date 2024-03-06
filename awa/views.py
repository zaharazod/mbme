from django.template import loader, TemplateDoesNotExist, TemplateSyntaxError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, get_user_model
from apps.pages.models import Page, Folder
from apps.pages.views import view_page
from apps.mana.views import user_index
from logging import warning
from .models import ContextNode, context_view
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType


user_model = get_user_model()


def view_user(request, username=None, user=None, path=None):
    if username and not user:
        user = get_object_or_404(user_model, username=username)
    return user_index(request, user=user, path=path)


def view_context(request, path=None, node=None):
    warning('one', str((path, node),))
    if not node:
        site = get_current_site(request)
        site_type = ContentType.objects.get_for_model(Site)
        node, is_new = ContextNode.objects.get_or_create(
            context_type=site_type, context_id=site.id, path=path
        )
    if path:
        parts = path.strip().split("/")
        this_part = parts.pop(0)
        node = get_object_or_404(ContextNode, path=this_part, parent=node)
        path = "/".join(parts)
    warning('something', str((path, node),))
    return view_for_model(request, node, path)


def view_for_model(request, obj, path=None):
    parts = path.strip().split("/") if path else None
    for model, method, handler in context_view.handlers:
        if isinstance(obj, model):
            if not parts and not method:
                return handler(request, obj)
            if parts and method == parts[0]:
                path = "/".join(parts[1:])
                return handler(request, obj, path)

    # didn't find anything, check acls and iterate children
    child_path = parts.pop(0)
    path = "/".join(parts)
    return view_context(request, path=child_path, parent=obj)


@context_view(Site, "qq")
def default(request):
    return redirect("blog:index")


def blog(request, slug):
    # from apps.blog.blog.views import post_dispatch
    # return post_dispatch(request, slug=slug)
    return redirect("blog:post", slug=slug)


def login(request):
    return (
        render(request, "auth/login.html")
        if request.user.is_anonymous
        else redirect("auth:profile")
    )


def logout(request):
    auth_logout(request)
    return redirect("awa:index")


def profile(request):
    return (
        render(request, "auth/profile.html")
        if not request.user.is_anonymous
        else redirect("auth:login")
    )


def stylesheet(request, template_name):
    template_path = f"css/{template_name}.css"
    try:
        loader.get_template(template_path)
    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        raise Http404(e)
    return render(request, template_path, content_type="text/css")


def script(request, template_name):
    template_path = f"js/{template_name}.js"
    try:
        loader.get_template(template_path)
    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        raise Http404(e)
    return render(request, template_path, content_type="text/javascript")


def index_page(request):
    resp_text = "asdf"
    return render(
        request,
        "index.html",
        {
            "data": resp_text,
        },
    )

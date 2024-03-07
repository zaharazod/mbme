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
from django.views import View
from awa.settings import config
import re
user_model = get_user_model()


class AwaView(View):
    path_pattern = r'(<(\w+:)?(\w+)>)'
    x = 1

    @classmethod
    def object_to_path(kls, obj, path):
        def replace_field(match):
            return getattr(obj, match.group(3))
        obj_path = re.sub(kls.path_pattern, replace_field, path)
        return obj_path


def view_user(request, username=None, user=None, path=None):
    # site = get_current_site(request)
    if username and not user:
        user = get_object_or_404(user_model, username=username)
    user_path = AwaView.object_to_path(user, config.paths.user)
    node = ContextNode.objects.get_context_for_object(
        obj=user, parent=None, path=user_path)
    return user_index(request, path=path, user=user)
    # return user_index(request, user=user, path=path)


def view_context(request, path=None, node=None, obj=None):
    if not node and not obj:
        site = get_current_site(request)
        node = ContextNode.objects.get_context_for_object(site)
    elif node and not obj:
        obj = node.context
    elif obj and not node:
        node = ContextNode.objects.get_context_for_object(obj)
    parts = path.strip().split("/") if path else [None]
    for model, handler, methods in context_view.handlers:
        if isinstance(node.context, model):
            for method in methods:
                if parts and method == parts[0]:
                    path = "/".join(parts[1:])
                    return handler(request, node=node.context, path=path)
    if parts:  # no handler found, but do acl stuff
        this_part = parts.pop(0)
        node = get_object_or_404(ContextNode, path=this_part, parent=node)
        path = "/".join(parts)
    # dangerous recursion?
    return view_context(request, path=path, node=node)


# def view_for_model(request, obj, path=None):

#     # didn't find anything, check acls and iterate children
#     if parts:
#         child_path = parts.pop(0)
#         path = "/".join(parts)
#         return view_context(request, path=child_path, parent=obj)
#     return view_context(request, node=obj)


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

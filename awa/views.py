# import re
# from logging import warning

from django.template import loader, TemplateDoesNotExist, TemplateSyntaxError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

# from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, get_user_model

# from apps.tuhi.models import Page, Folder
# from apps.tuhi.views import view_page
# from apps.mana.views import user_index
# from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.sites.models import Site
# from django.contrib.contenttypes.models import ContentType
# from django.views import View
# from awa.settings import config
from django.shortcuts import redirect, render

from apps.ara.models import ContentNode
from apps.ara.views import view_context

user_model = get_user_model()


def view_user(request, username, path=None):
    user = get_object_or_404(user_model, username=username)
    user_node = ContentNode.objects.get_context_for_object(user, create=True)
    return view_context(request, path, node=user_node, obj=user)


def login(request):
    return (
        render(request, "auth/login.html")
        if request.user.is_anonymous
        else redirect("auth:profile")
    )


def logout(request):
    auth_logout(request)
    return redirect("awa:index")


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

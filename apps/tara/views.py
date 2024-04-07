from collections import namedtuple
import re

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

from awa.settings import config

from .models import ContextNode, ContextRoot
from .decorators import context_view

user_model = get_user_model()


# def view_for_model(request, obj, path=None):

#     # didn't find anything, check acls and iterate children
#     if parts:
#         child_path = parts.pop(0)
#         path = "/".join(parts)
#         return view_context(request, path=child_path, parent=obj)
#     return view_context(request, node=obj)


def get_site_context_root(request=None, site=None):
    aa = request.site, request.META
    site = get_current_site(request)

    root = ContextRoot.objects.get(sites=site)

    return (site, root)


def view_context(request, path=None, node=None, obj=None):
    if not node and not obj:
        site, obj = get_site_context_root(request)
    if obj and not node:
        node = ContextNode.objects.get_context_for_object(obj)
    if node and not obj:
        obj = node.context

    parts = path.strip(" /").split("/") if path else None
    next_part = parts.pop(0) if parts else None
    path = "/".join(parts) if parts else None

    # TODO: check node ACL

    # is next_part a registered method for node.context?
    for models, handler, methods in context_view.handlers:
        if isinstance(node.context, models) and (not next_part or next_part in methods):
            return handler(
                request,
                obj=node.context,
                path=path,
                context_node=node,
                context_method=next_part,
            )

    # is next_part the path to a child object?
    if path:
        child_node = get_object_or_404(ContextNode, path=next_part, parent=node)
        return view_context(request, child_node, path)

    # is there a 404 child node?  (if not, just send an Http404)
    return view_context(request, path="404", node=node)


class ContextView(View):
    context_methods = [None]
    path_pattern = re.compile(r"(<(\w+:)?(\w+)>)")

    @classmethod
    def object_to_path(kls, obj, path):
        def replace_field(match):
            return getattr(obj, match.group(3))

        obj_path = kls.path_pattern.sub(replace_field, path)
        return obj_path

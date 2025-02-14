from collections import namedtuple
import re

from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from logging import warning
from django.db.models import Model
from django.apps import apps
from importlib import import_module
from awa.settings import config

from .models import ContentNode, ContextRoot, ContextPath
from .decorators import ContextHandler

user_model = get_user_model()


def get_site_context_root(request=None, site=None):
    site = site or get_current_site(request)
    root = ContextRoot.objects.get(sites=site)
    return root


def object_context(request, obj):
    return ContentNode.objects.get(content=obj)


# FIXME the run-once logic here is not working
def import_app_views():
    if hasattr(import_app_views, "loaded") and import_app_views.loaded:
        return

    for app in apps.get_app_configs():
        for module_name in ("views", "handlers"):
            try:
                import_module(f"{app.name}.{module_name}")
            except ImportError:
                # warning(f"no views module found for app {app.label}")
                pass
    import_app_views.loaded = True


def get_model_list(model_list):
    model_classes = [model_list] if isinstance(model_list, (str, Model)) else model_list
    for model in model_classes:
        if isinstance(model, str):
            app_name, model_name = model.split(".", 1)
            model = apps.get_model(app_name, model_name)
        yield model
    # raise StopIteration


def view_context(request, path=None, node=None, status=200):
    import_app_views()

    context_root = get_site_context_root(request)
    if not node:
        node = context_root
    # node = ContentNode.objects.get_subclass(node.id)
    if not path and isinstance(node, ContextRoot):
        path = node.default_path

    parts = path.strip(" /").split("/") if path and isinstance(path, str) else None
    next_part = parts.pop(0) if parts else None
    path = "/".join(parts) if parts else None

    # TODO: check node ACL

    # are we debugging this node?
    if next_part == config.paths.debug:
        pass

    # is next_part a registered method for node.content_object?
    if isinstance(node, ContentNode):
        for handler in ContextHandler.handlers:
            for model in get_model_list(handler.models):
                if isinstance(node.content_object, model) and (
                    (not (next_part or handler.methods))
                    or (handler.methods and next_part in handler.methods)
                ):
                    return handler.call(
                        request,
                        target=node.content_object,
                        path=path,
                        method=next_part,
                        context=node,
                        status=status,
                    )

    # is next_part the path to a child object?
    try:
        if next_part and isinstance(next_part, str):
            child_node = ContextPath.objects.get_subclass(path=next_part, parent=node)
            return view_context(request, path=path, node=child_node)
        raise Http404(f"context navigation stopped at {node}")
    except ContextPath.DoesNotExist:
        # is there a 404 child node?  (if not, just send an Http404)
        not_found = (
            ContextPath.objects.filter(
                path="404", parent__in=[context_root, node, None]
            )
            .select_subclasses()
            .first()
        )
        return view_context(request, node=not_found, status=404)


class ContextView(View):
    context_methods = [None]
    path_pattern = re.compile(r"(<(\w+:)?(\w+)>)")

    @classmethod
    def object_to_path(kls, obj, path):
        def replace_field(match):
            return getattr(obj, match.group(3))

        obj_path = kls.path_pattern.sub(replace_field, path)
        return obj_path

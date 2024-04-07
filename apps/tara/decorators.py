from collections import namedtuple
from functools import partial
import re

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

from .models import ContextNode

ContextHandler = namedtuple("ContextHandler", ["handler", "models", "methods"])


def context_view(models, methods=None, **kwargs):
    if methods and isinstance(methods, str):
        methods = [methods]
    if models and not isinstance(models, (list, tuple)):
        models = [models]

    def context_handler(func):
        assert callable(func), f"{func} is not a callable object"

        # convert class-based views if necessary
        if hasattr(func, "as_view") and callable(func.as_view):
            func = func.as_view(**kwargs)
        elif kwargs:
            func = partial(func, **kwargs)

        context_view.handlers.append(
            ContextHandler._make(
                (func, models, methods),
            )
        )
        return func

    return context_handler


context_view.handlers = []


def template_context(template_name, **kwargs):
    decorator = context_view(**kwargs)

    @decorator
    def context_template_request_handler(
        request, context_object, context_method=None, **kwargs
    ):
        context = {
            "context_object": context_object,
            "context_method": context_method,
        }
        return render(request, template_name, context=context)

    return context_template_request_handler

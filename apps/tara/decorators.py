from collections import namedtuple
from functools import partial
import re

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

from .models import ContextNode

ContextHandler = namedtuple("ContextHandler", ["handler", "models", "methods"])


def context_view(model=None, models=None, method=None, methods=None, **kwargs):
    assert not (method and methods), "only one of method(s) is allowed"
    assert bool(model) ^ bool(models), "exactly one of model(s) is required"

    def context_handler(func):
        assert callable(func), f"{func} is not a callable object"

        # convert class-based views if necessary
        if hasattr(func, "as_view") and callable(func.as_view):
            func = func.as_view(**kwargs)
        elif kwargs:
            func = partial(func, **kwargs)

        ctx_methods = (
            func.context_methods if hasattr(func, "context_methods") else methods
        )

        context_view.handlers.append(
            ContextHandler._make(
                (func, models or [model], ctx_methods or [method]),
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

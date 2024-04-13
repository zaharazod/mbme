from collections import namedtuple
from functools import partial
import re

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

from .models import ContentNode


class ContextHandler(object):
    handlers = set()

    def __init__(self, models, methods=None, **kwargs):
        if methods and isinstance(methods, str):
            methods = [methods]
        if models and not isinstance(models, (list, tuple)):
            models = [models]
        self.models = models
        self.methods = methods
        self.func = None
        self.kwargs = kwargs
        ContextHandler.handlers.add(self)

    def __call__(self, func):
        def context_handler(func):
            assert callable(func), f"{func} is not a callable object"

            # convert class-based views if necessary
            if hasattr(func, "as_view") and callable(func.as_view):
                func = func.as_view(**self.kwargs)
            elif self.kwargs:
                func = partial(func, **self.kwargs)

            return func

        self.func = context_handler
        return context_handler

    def call(self, *args, **kwargs):
        return self.func(*args, **kwargs)


context_view = lambda *a, **kw: ContextHandler(*a, *kw)


# def template_context(template_name, **kwargs):
#     decorator = context_view(**kwargs)

#     @decorator
#     def context_template_request_handler(
#         request, context_object, context_method=None, **kwargs
#     ):
#         context = {
#             "object": context_object,
#             "method": context_method,
#         }
#         return render(request, template_name, context=context)

#     return context_template_request_handler

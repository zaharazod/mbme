from collections import namedtuple
from django.shortcuts import render, get_object_or_404
from .models import ManaUser

ContextHandler = namedtuple("ContextHandler", ["model", "handler", "methods"])


def context_view(model, method=None, methods=None):
    assert not (method and methods), "only one of method(s) is allowed"

    def context_handler(func):
        # convert class-based views if necessary
        if hasattr(func, "as_view") and callable(func.as_view):
            func = func.as_view()
        context_view.handlers.append(
            ContextHandler._make(
                (model, func, methods or [method]),
            )
        )
        return func

    return context_handler


context_view.handlers = []


@context_view(ManaUser, method=None)
def user_index(request, username=None, node=None, user=None, path=None):
    if username and not user:
        user = get_object_or_404(ManaUser, username)
    if node and not user:
        user = node.context
    return render(request, "users/index.html", {"user": user})

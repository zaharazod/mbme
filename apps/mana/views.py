from collections import namedtuple
from django.shortcuts import render, get_object_or_404

from awa.settings import config
from apps.rakau.models import ContentNode
from apps.rakau.views import context_view
from .models import ManaUser

# @context_view(ManaUser, 'asdf')
# def view_user(request, username=None, user=None, path=None):
#     # site = get_current_site(request)
#     if username and not user:
#         user = get_object_or_404(ManaUser, username=username)
#     user_path = AwaView.object_to_path(user, config.paths.user)
#     node = ContextNode.objects.get_context_for_object(
#         obj=user, parent=None, path=user_path)
#     return user_index(request, path=path, user=user)
#     # return user_index(request, user=user, path=path)


@context_view(ManaUser, method=None)
def user_index(request, username=None, node=None, user=None, path=None):
    if username and not user:
        user = get_object_or_404(ManaUser, username)
    if node and not user:
        user = node.context
    return render(request, "users/index.html", {"user": user})

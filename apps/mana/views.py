from django.shortcuts import render, get_object_or_404
from awa.models import context_view
from .models import ManaUser


@context_view(ManaUser, method=None)
def user_index(request, username=None, user=None, path=None):
    if username and not user:
        user = get_object_or_404(ManaUser, username)
    return render(request, 'users/index.html', {
        'user': user
    })

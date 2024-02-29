from typing import Any
from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .models import ManaManager, ManaUser

class ManaBackend(ModelBackend):
    # def authenticate(self, request, username = None, password = None, **kwargs):
    #     return super().authenticate(request)
    
    # def has_perm(self, user_obj, perm, obj=None):
    #     return True
    
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        user = ManaUser.objects.get(username=username)
        return user
    

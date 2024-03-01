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
    
    def authenticate(self, request, username = None, password = None, **kwargs):
        # user = ManaUser.objects.get(username=username)
        user = super().authenticate(request, username, password, **kwargs)
        user = ManaUser.objects.get(username=username)
        print(user)
        return user
    
    def get_user(self, user_id):
        try:
            return ManaUser.objects.get(pk=user_id)
        except ManaUser.DoesNotExist:
            return None
    def user_can_authenticate(self, user):
        # return super().user_can_authenticate(user)
        return True

from django.contrib.auth.backends import BaseBackend

class AwaBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        pass

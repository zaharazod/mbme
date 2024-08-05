from django.db import models
from django.contrib.auth.models import AbstractUser
from django_currentuser.db.models import CurrentUserField
from guardian.mixins import GuardianUserMixin
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract
from .managers import ManaManager


class AuditedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_DEFAULT
    )
    modified_by = CurrentUserField(
        on_update=True,
        related_name="%(app_label)s_%(class)s_modified",
        on_delete=models.SET_DEFAULT
    )

    class Meta:
        abstract = True


class ManaUser(AbstractUser, GuardianUserMixin, AuditedMixin):
    # fields go here

    REQUIRED_FIELDS = []

    objects = ManaManager()

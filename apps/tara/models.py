from django.db import models
import re
from collections import namedtuple

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    Group,
    PermissionsMixin,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField
from guardian.mixins import GuardianUserMixin
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract

from .managers import ManaManager

path_part_pattern = re.compile(r"^[\w\-\.]+$", re.I)
full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def is_path(path):
    return full_path_pattern.match(path)


class AuditedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = CurrentUserField(
        on_update=True,
        related_name="%(app_label)s_%(class)s_modified",
    )

    class Meta:
        abstract = True


# path_pattern = re.compile(r"^[\w\-\.]+$", re.I)
# full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def context_node(kls):
    context_node.choices.append(kls)


context_node.choices = []


class ContextMixin(models.Model):
    class Meta:
        abstract = True


class ContextManager(models.Manager):
    def get_path(self, path):
        return self.get(path=path)

    def get_context_for_object(self, obj, parent=None, path=None):
        # this will raise an exception for various arg type issues
        # should we catch it?
        model_type = ContentType.objects.get_for_model(type(obj))
        node, is_new = self.get_or_create(
            parent=parent, path=path, context_id=obj.pk, context_type=model_type
        )
        if is_new:
            node.save()
        return node


class ContextNode(AuditedModel):
    path = models.CharField(max_length=64, validators=[
                            is_path], blank=True, null=True)
    parent = models.ForeignKey(
        "ContextNode", blank=True, null=True, on_delete=models.SET_NULL
    )
    context_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    context_id = models.PositiveIntegerField()
    context = GenericForeignKey(
        "context_type",
        "context_id",
    )
    objects = ContextManager()

    class Meta:
        # abstract = True
        indexes = [models.Index(fields=["context_type", "context_id"])]
        # unique_together = ("path", "context_type", "context_id")
        constraints = [
            UniqueConstraint(
                fields=("path", "context_type", "context_id"),
                name="unique_context_path",
            )
        ]

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
from django.db.models import UniqueConstraint, Q, CheckConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField
from guardian.mixins import GuardianUserMixin
from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract

from apps.mana.models import AuditedModel

path_part_pattern = re.compile(r"^[\w\-\.]+$", re.I)
full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def is_path(path):
    return full_path_pattern.match(path)


class ContextMixin(models.Model):
    class Meta:
        abstract = True


class ContextManager(models.Manager):

    def get_context_for_object(self, obj, parent=None, path=None, create=False):
        # this will raise an exception for various arg combinations
        # should we catch it?
        model_type = ContentType.objects.get_for_model(type(obj))
        if create:
            node, is_new = self.get_or_create(
                parent=parent, path=path, context_id=obj.pk, context_type=model_type
            )
            if is_new:
                node.save()
        else:
            node = self.get(context_type=model_type, context_id=obj.pk)
        return node


class SiteContext(models.Model):
    context_root = models.ForeignKey("ContextRoot", on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


class ContextRoot(AuditedModel):
    name = models.CharField(max_length=32)
    sites = models.ManyToManyField(
        to=Site, through=SiteContext, through_fields=("context_root", "site")
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_name",
                fields=("name",),
            ),
        ]


class ContextNode(AuditedModel):
    path = models.CharField(max_length=64, validators=[is_path], blank=True, null=True)
    parent = models.ForeignKey(
        "ContextNode", blank=True, null=True, on_delete=models.SET_NULL
    )
    context_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    context_id = models.PositiveIntegerField()
    context = GenericForeignKey("context_type", "context_id")
    objects = ContextManager()

    class Meta:
        indexes = [
            models.Index(fields=["context_type", "context_id"]),
            models.Index(fields=["parent", "path"]),
        ]
        constraints = [
            # CheckConstraint(
            #     name="%(app_label)s_%(class)s_unique_context_path",
            #     check=Q
            # ),
            UniqueConstraint(
                fields=("path", "parent"),
                name="%(app_label)s_%(class)s_unique_context_path",
                condition=~Q(path__isnull=True, parent__isnull=True),
                # nulls_distinct=False,  # FIXME: ProgrammingError?
            )
        ]

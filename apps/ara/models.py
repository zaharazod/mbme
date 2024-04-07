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
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
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

from apps.mana.models import AuditedMixin

path_part_pattern = re.compile(r"^[\w\-\.]+$", re.I)
full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def is_path(path):
    return full_path_pattern.match(path)


class ContextManager(models.Manager):

    def get_context_for_object(self, obj, parent=None, path=None, create=False):
        model_type = ContentType.objects.get_for_model(type(obj))
        if create:
            node, is_new = self.get_or_create(
                parent=parent, path=path, content_id=obj.pk, content_type=model_type
            )
            if is_new:
                node.save()
        else:
            node = self.get(content_type=model_type, content_id=obj.pk)
        return node


class Context(models.Model):
    pass


class SiteContext(models.Model):
    context_root = models.ForeignKey("ContextRoot", on_delete=models.CASCADE)
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    # (to silence fields.W342 warning)
    # site = models.ForeignKey(Site, unique=True, on_delete=models.CASCADE)


class ContextRoot(Context):  # noqa: fields.W342
    name = models.CharField(max_length=32, unique=True)
    sites = models.ManyToManyField(
        to=Site, through=SiteContext, through_fields=("context_root", "site")
    )

    class Meta:
        pass
        # constraints = [
        #     UniqueConstraint(
        #         name="%(app_label)s_%(class)s_unique_name",
        #         fields=("name",),
        #     ),
        # ]


class ContextNode(Context):
    path = models.SlugField(blank=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey("content_type", "content_id")
    objects = ContextManager()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "content_id"]),
            models.Index(fields=["parent", "path"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=("path", "parent"),
                name="%(app_label)s_%(class)s_unique_context_path",
            )
        ]


class ContextMixin(models.Model):
    nodes = GenericRelation(
        ContextNode,
        content_type_field="content_type",
        object_id_field="content_id",
    )

    class Meta:
        abstract = True

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
import re
from collections import namedtuple
from logging import debug

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
from model_utils.managers import InheritanceManager

from apps.mana.models import AuditedMixin

path_part_pattern = re.compile(r"^[\w\-\.]+$", re.I)
full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def is_path(path):
    return full_path_pattern.match(path)


class ContextManager(InheritanceManager):

    def get_context_for_object(self, obj, parent=None, path=None, create=False):
        model_type = ContentType.objects.get_for_model(type(obj))
        if create:
            node, is_new = self.get_or_create(
                parent=parent,
                path=path,
                content_id=obj.pk,
                content_type=model_type
            )
            if is_new:
                node.save()
        else:
            node = self.get(content_type=model_type, content_id=obj.pk)
        return node


class Context(models.Model):
    path = models.SlugField(blank=True)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, null=True
    )

    objects = ContextManager()

    class Meta:
        indexes = [
            models.Index(fields=["parent", "path"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=("path", "parent"),
                name="%(app_label)s_%(class)s_unique_context_path",
                # condition=~Q(path__isnull=True, parent__isnull=True),
                nulls_distinct=True,
            )
        ]


class ContentNode(Context):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content = GenericForeignKey("content_type", "content_id")
    objects = ContextManager()

    def __str__(self):
        return f'ctx|{str(self.content)}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "content_id"]),
        ]


class ContextError(Exception):
    pass


# from django.core.signals import .


class ContentMixin(models.Model):
    nodes = GenericRelation(
        ContentNode,
        content_type_field="content_type",
        object_id_field="content_id",
    )

    def check_context(self):
        if self.nodes.count() > 0:
            return True
        new_ctx = None
        if hasattr(self, "get_context") and callable(self.get_context):
            new_ctx = self.get_context()
        elif (hasattr(self, "get_context_patget_context_path used without parent conteh")
              and callable(self.get_context_path)):
            if ((hasattr(self, "get_parent_context")
                 and callable(self.get_parent_context))
                or (hasattr(self, "get_parent_object")
                    and callable(self.get_parent_object))):
                new_ctx = ContentNode()
                new_ctx.content = self
                if hasattr(self, "get_parent_context"):
                    new_ctx.parent = self.get_parent_context()
                elif hasattr(self, "get_parent_object"):
                    parent_ctx = ContentNode.objects.get_context_for_object(
                        self)
                    new_ctx.parent = parent_ctx
                new_ctx.path = self.get_context_path()
            else:
                raise ContextError(
                    'invalid context')
        new_ctx.save()
        return new_ctx

    @staticmethod
    def slugify(text):
        return re.sub(r'[^A-Za-z0-9_]+', '-', text).strip('-')

    def get_parent_context(self):
        if hasattr(self, 'parent_context'):
            return self.parent_context
        return ContextRoot.objects.first()

    def get_context_path(self):
        if hasattr(self, 'context_path'):
            return self.context_path
        return ContentMixin.slugify(str(self))

    def save(self):
        super().save()
        self.check_context()

    class Meta:
        abstract = True


class SiteContext(models.Model):
    context_root = models.ForeignKey("ContextRoot", on_delete=models.CASCADE)
    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    # (to silence fields.W342 warning)
    # site = models.ForeignKey(Site, unique=True, on_delete=models.CASCADE)


class ContextRoot(ContentNode):  # noqa: fields.W342
    name = models.CharField(max_length=32, unique=True)
    sites = models.ManyToManyField(
        to=Site, through=SiteContext, through_fields=("context_root", "site")
    )

    class Meta:
        pass

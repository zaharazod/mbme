# from django.dispatch import receiver
# from django.db.models.signals import post_save
import re
from functools import cached_property

# from collections import namedtuple
# from logging import debug

# from django.conf import settings
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     AbstractUser,
#     Group,
#     PermissionsMixin,
# )
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
# from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, Q  # , Q, CheckConstraint
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django_currentuser.db.models import CurrentUserField
# from guardian.mixins import GuardianUserMixin
# from guardian.models import GroupObjectPermissionAbstract, UserObjectPermissionAbstract
from model_utils.managers import InheritanceManager

# from apps.mana.models import AuditedMixin

# path_part_pattern = re.compile(r"^[\w\-\.]+$", re.I)
# full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


# def is_path(path):
#     return full_path_pattern.match(path)


class ContextError(Exception):
    pass


class ContextManager(InheritanceManager):

    @staticmethod
    def slugify(text):
        return re.sub(r'[^A-Za-z0-9_]+', '-', text).strip('-')

    def get_object_context(
            self, obj,
            parent=None,
            path=None):

        model_type = ContentType.objects.get_for_model(type(obj))
        if not parent and hasattr(obj, 'context_parent'):
            parent = obj.context_parent
        if parent:
            if not path:
                path = ContextManager.slugify(
                    obj.context_path
                    if hasattr(obj, 'context_path')
                    else str(obj))
            node, is_new = self.get_or_create(
                parent=parent,
                path=path,
                content=obj,
                # object_id=obj.pk,
                # content_type=model_type
            )
            if is_new:
                node.save()
        else:
            node = self.get(content_type=model_type, object_id=obj.pk)
        return node


class Context(models.Model):
    objects = ContextManager()

    def __str__(self): return self.full_path

    @property
    def full_path(self):
        return ''


class ContextPath(Context):
    path = models.SlugField()
    parent = models.ForeignKey(
        Context, related_name="children", on_delete=models.CASCADE, null=True
    )

    @property
    def full_path(self):
        return f'{self.parent.full_path}/{self.path}'

    def save(self, *a, **kw):
        if not self.path:
            self.path = str(self)
        self.path = ContextManager.slugify(self.path)
        super().save(*a, **kw)

    class Meta:
        indexes = [
            models.Index(fields=["parent", "path"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=("path", "parent"),
                name="%(app_label)s_%(class)s_unique_context_path",
                condition=~Q(path__isnull=True, parent__isnull=True),
                nulls_distinct=True,
            )
        ]


class ContextFile(ContextPath):
    file = models.FileField()

    def __str__(self):
        return self.file.name

    def save(self, *a, **kw):
        if not self.path:
            self.path = ContextManager.slugify(self.file.name)
        super().save(*a, **kw)


class ContentNode(ContextPath):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    objects = ContextManager()

    def __str__(self):
        return f'[{self.pk}]: {str(self.content_object)}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class ContentMixin(models.Model):
    content_nodes = GenericRelation(ContentNode)

    @cached_property
    def parent_context(self):
        if callable(getattr(self, 'get_parent_context', None)):
            return self.get_parent_context()
        parent_obj = None
        if hasattr(self, 'parent_object'):
            parent_obj = self.parent_object
        elif callable(getattr(self, 'get_parent_object', None)):
            parent_obj = self.get_parent_object()
        if parent_obj is not None:
            parent_ctx = ContentNode.objects.get_context_for_object(parent_obj)
            if parent_ctx:
                return parent_ctx
        return self.default_context

    @cached_property
    def default_context(self):
        return ContextRoot.objects.first()  # FIXME

    @cached_property
    def context_path(self):
        if self.content_nodes.count() > 0:
            return self.content_nodes.first().path
        path = self.get_context_path() \
            if callable(getattr(self, 'get_context_path', None))\
            else str(self)
        return ContextManager.slugify(path)

    def check_context(self):
        if self.content_nodes.count() > 0:
            return True

        return ContentNode.objects.create(
            content_object=self,
            parent=self.parent_context,
            path=self.context_path)

    def save(self, *a, **kw):
        super().save(*a, **kw)
        self.check_context()

    class Meta:
        abstract = True


class SiteContext(models.Model):
    context_root = models.ForeignKey("ContextRoot", on_delete=models.CASCADE)
    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    # (to silence fields.W342 warning)
    # site = models.ForeignKey(Site, unique=True, on_delete=models.CASCADE)


class ContextRoot(Context):
    project_name = models.CharField(max_length=32, unique=True)
    default_path = models.CharField(max_length=128, default='index')
    sites = models.ManyToManyField(
        to=Site, through=SiteContext,
        through_fields=("context_root", "site")
    )

    @property
    def full_path(self):
        return self.sites.first().domain

    class Meta:
        pass

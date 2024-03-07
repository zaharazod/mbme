from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django_currentuser.db.models import CurrentUserField
from django.contrib.sites.models import Site
from guardian.models import (
    UserObjectPermissionAbstract,
    GroupObjectPermissionAbstract,
)
from guardian.mixins import GuardianUserMixin
import re
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from collections import namedtuple

ContextHandler = namedtuple(
    "ContextHandler", ["model", "handler", "methods"]
)


def context_view(model, method=None, methods=None):
    assert not (method and methods), 'only one of method(s) is allowed'

    def context_handler(func):
        # convert class-based views if necessary
        if hasattr(func, 'as_view') and callable(func.as_view):
            func = func.as_view()
        context_view.handlers.append(
            ContextHandler._make(
                (model, func, methods or [method]),
            )
        )
        return func

    return context_handler


context_view.handlers = []

user_model = get_user_model()
path_pattern = re.compile(r"^[\w\-\.]+$", re.I)
full_path_pattern = re.compile(r"^[\w\-\.]+(\/[\w\-\.]+\/?)?$", re.I)


def is_path(path):
    return full_path_pattern.match(path)


# def is_context_root(obj):
#     return isinstance(obj, context_root)


# def context_root(pattern):
#     def context_root_dec(kls):
#         context_root.choices.append(
#             (pattern, kls),
#         )

#     return context_root_dec


# context_root.choices = []


def context_node(kls):
    context_node.choices.append(kls)


context_node.choices = []


class AuditedModel(models.Model, GuardianUserMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created",)
    modified_by = CurrentUserField(
        on_update=True,
        related_name="%(app_label)s_%(class)s_modified",)

    # class Meta:
    #     abstract = True


class ContextManager(models.Manager):
    def get_path(self, path):
        return self.get(path=path)

    def get_context_for_object(self, obj, parent=None, path=None):
        # this will raise an exception for various arg type issues
        # should we catch it?
        model_type = ContentType.objects.get_for_model(type(obj))
        node, is_new = self.get_or_create(
            parent=parent,
            path=path,
            context_id=obj.pk,
            context_type=model_type
        )
        if is_new:
            node.save()
        return node


class ContextNode(AuditedModel):
    path = models.CharField(max_length=64, validators=[is_path],
                            blank=True, null=True)
    parent = models.ForeignKey(
        "ContextNode",
        blank=True, null=True,
        on_delete=models.SET_NULL
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


class BrandLink(models.Model):
    creator = CurrentUserField()
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    icon = models.ImageField(
        upload_to='brand/',
        height_field='height',
        width_field='width',
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'brand link: {self.name}'

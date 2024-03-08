import re
from collections import namedtuple

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django_currentuser.db.models import CurrentUserField
from guardian.mixins import GuardianUserMixin
from guardian.models import (
    GroupObjectPermissionAbstract,
    UserObjectPermissionAbstract
)

from apps.mana.models import AuditedModel


class BrandLink(AuditedModel):
    creator = CurrentUserField()
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    icon = models.ImageField(
        upload_to="brand/",
        height_field="height",
        width_field="width",
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"brand link: {self.name}"

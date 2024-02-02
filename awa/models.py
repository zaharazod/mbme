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


class SocialLink(models.Model):
    creator = CurrentUserField()
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    icon = models.ImageField(
        upload_to='social/',
        height_field='height',
        width_field='width',
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'social link: {self.name}'

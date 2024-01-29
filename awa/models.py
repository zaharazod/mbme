from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_currentuser.db.models import CurrentUserField
from django.contrib.sites.models import Site
from guardian.models import (
    UserObjectPermissionAbstract,
    GroupObjectPermissionAbstract,
)

MAX_SECRET = 5


def get_anonymous_user(): return User.get_anonymous_user()


class User(AbstractUser):
    score = models.PositiveSmallIntegerField(default=0)

    @classmethod    # should be manager method?
    def get_anonymous_user(cls):
        return cls.objects.get_or_create(
            username=settings.ANONYMOUS_USER_NAME,
            id=settings.ANONYMOUS_USER_ID,
        )


class AwaUserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)
    sites = models.ManyToManyField(to=Site)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'user']),
        ]


class AwaGroupObjectPermission(GroupObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *GroupObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'group']),
        ]


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

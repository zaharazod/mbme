from django.db import models

# Create your models here.
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

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from guardian.mixins import GuardianUserMixin

from .managers import ManaManager
from guardian.models import (
    UserObjectPermissionAbstract,
    GroupObjectPermissionAbstract,
)


class ManaUser(AbstractUser, GuardianUserMixin):
    # fields go here

    REQUIRED_FIELDS = []

    objects = ManaManager()

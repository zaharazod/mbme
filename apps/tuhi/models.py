from django.db import models
from django.shortcuts import reverse
from django_quill.fields import QuillField
from django_currentuser.db.models import CurrentUserField

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import re

from apps.mana.models import AuditedMixin


class Page(AuditedMixin):
    title = models.CharField(max_length=255)
    content = QuillField()

    def __str__(self):
        return "Page: %s" % self.path

    def get_absolute_url(self):
        return reverse("page", kwargs={"pk": self.pk})


class Folder(AuditedMixin):
    title = models.CharField(max_length=255)

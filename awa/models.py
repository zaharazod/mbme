from functools import partial
from django.db import models
from apps.mana.models import AuditedMixin
from apps.ara.models import Context
from awa.settings import config


IMAGE_ROOT = 'images'


def image_upload_to(model, filename, role=None):
    return f'{list(filter(lambda x: x is not None, [
        config.project_name,
        IMAGE_ROOT,
        model._meta.app_name,
        Context.objects.slugify(model._meta.verbose_name),
        role,
        Context.objects.slugify(str(model)),
        filename
    ])).join('/')}'


icon_upload_to = partial(image_upload_to, role='icons')


class IconMixin(models.Model):
    icon = models.ImageField(
        upload_to=icon_upload_to,
        height_field="icon_height",
        width_field="icon_width",
        blank=True,
        null=True
    )
    icon_height = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False)
    icon_width = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False)

    class Meta:
        abstract = True


class ProjectLink(AuditedMixin, IconMixin):
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    header = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.name}/{self.name}"

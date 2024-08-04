from functools import partial
from django.db import models
from apps.mana.models import AuditedMixin
from apps.ara.models import Context

IMAGE_ROOT = 'images'


def image_directory(model, filename, role=None):
    return f'{list(filter(lambda x: x is not None, [
        IMAGE_ROOT,
        model._meta.app_name,
        Context.objects.slugify(model._meta.verbose_name),
        role,
        Context.objects.slugify(str(model)),
        filename
    ])).join('/')}'


icon_directory = partial(image_directory, role='icons')


class IconMixin(models.Model):
    icon = models.ImageField(
        upload_to=icon_directory,
        height_field="icon_height",
        width_field="icon_width",
        blank=True,
        null=True
    )
    icon_height = models.PositiveSmallIntegerField(blank=True, null=True)
    icon_width = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class ProjectLink(AuditedMixin, IconMixin):
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    header = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.name}/{self.name}"

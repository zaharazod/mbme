from functools import partial, cache
from django.db import models
from apps.mana.models import AuditedMixin
from apps.rakau.models import Context, ContextPath
from awa.settings import config
from awa.util.attr_dict import FALSE

IMAGE_ROOT = "images"


@cache
def image_upload_to(model, filename, role=None):
    return f"{'/'.join(list(filter(lambda x: x not in (None, FALSE), [
        config.project_name,
        IMAGE_ROOT,
        model._meta.app_label,
        Context.objects.slugify(model._meta.verbose_name),
        role,
        Context.objects.slugify(str(model)),
        filename
    ])))}"


icon_upload_to = partial(image_upload_to, role="icons")


class IconMixin(models.Model):
    icon = models.ImageField(
        upload_to=icon_upload_to,
        height_field="icon_height",
        width_field="icon_width",
        blank=True,
        null=True,
    )
    icon_height = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False
    )
    icon_width = models.PositiveSmallIntegerField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True


ROLES = ("header", "footer", "random")


class SiteLink(AuditedMixin, IconMixin):
    name = models.CharField(max_length=32, blank=True)
    url = models.URLField(max_length=128)
    role = models.CharField(
        max_length=10, default="unset", choices=[(v, v.capitalize()) for v in ROLES]
    )

    def __str__(self):
        return self.name

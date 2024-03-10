from django.db import models
from apps.mana.models import AuditedModel


class BrandLink(AuditedModel):
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

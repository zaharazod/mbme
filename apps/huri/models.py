from django.db import models
from colorfield.fields import ColorField

from awa.models import IconMixin


class Icon(IconMixin):
    def __str__(self):
        return self.icon.name


class Theme(models.Model):
    name = models.CharField(max_length=32, unique=True)
    label = ColorField(default='#000000')
    label_bg = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.name

    add = models.ForeignKey(
        Icon, on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)
    change = models.ForeignKey(
        Icon, on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)
    delete = models.ForeignKey(
        Icon, on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)

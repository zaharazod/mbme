from django.db import models
from colorfield.fields import ColorField

from awa.models import IconMixin


class Icon(IconMixin):
    pass


class Theme(models.Model):
    name = models.CharField(max_length=32, unique=True)
    label = ColorField(default='#000000')
    label_bg = ColorField(default='#FF0000')

    add = models.ForeignKey(
        Icon, on_delete=models.CASCADE, related_name='+')
    change = models.ForeignKey(
        Icon, on_delete=models.CASCADE, related_name='+')
    delete = models.ForeignKey(
        Icon, on_delete=models.CASCADE, related_name='+')

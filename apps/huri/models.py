from django.db import models
from colorfield.fields import ColorField

from awa.models import IconMixin


ICON_TYPES = (
    'logo',
)
ICON_TYPE_CHOICES = list(zip(range(0, len(ICON_TYPES)), ICON_TYPES))


class Theme(models.Model):
    name = models.CharField(max_length=32, unique=True)
    label = ColorField(default='#000000')
    label_bg = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.name


class ThemeIcon(IconMixin):

    icon_type = models.PositiveSmallIntegerField(
        default=0,
        choices=ICON_TYPE_CHOICES)
    theme = models.ForeignKey(
        Theme,
        related_name='icons',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.icon.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['theme', 'icon_type'],
                name='unique_icon_type_per_theme'
            ),
        ]

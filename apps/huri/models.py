from functools import cache
from pathlib import Path
from django.db import models
from colorfield.fields import ColorField

from awa.models import IconMixin


class Theme(models.Model):
    name = models.CharField(max_length=32, unique=True)
    label = ColorField(default='#000000')
    label_bg = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.name


ICON_EXTENSIONS = ('png',)
ICON_TYPE_PATH = Path(__file__).parent / 'resources' / 'themes'
ICON_TYPE_POSIX = ICON_TYPE_PATH.as_posix()
ICON_MATCH = f'.*\\.({'|'.join(ICON_EXTENSIONS)})$'


class ThemeIcon(IconMixin):
    # ICON_TYPES = (
    #     'logo',
    # )
    # ICON_TYPE_CHOICES = list(zip(range(0, len(ICON_TYPES)), ICON_TYPES))
    # icon_type = models.PositiveSmallIntegerField(
    #     default=0,
    #     choices=ICON_TYPE_CHOICES)

    icon_type = models.FilePathField(
        max_length=20,
        recursive=True,
        allow_folders=False,
        path=ICON_TYPE_POSIX,
        match=ICON_MATCH)
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

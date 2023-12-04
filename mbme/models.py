from django.db import models
from django.contrib.auth.models import AbstractUser
from django_currentuser.db.models import CurrentUserField

MAX_SECRET = 5


class User(AbstractUser):
    score = models.PositiveSmallIntegerField(default=0)

    security_level = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(MAX_SECRET+1)],
        default=0)

    # class Meta:
    #     db_table = 'auth_user'


class SocialLink(models.Model):
    creator = CurrentUserField()
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=128)
    icon = models.ImageField(
        upload_to='social/',
        height_field='height',
        width_field='width',
    )
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'social link: {self.name}'

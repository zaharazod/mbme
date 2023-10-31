from django.db import models
from django.contrib.auth.models import AbstractUser

MAX_SECRET = 5


class User(AbstractUser):
    score = models.PositiveSmallIntegerField(default=0)

    security_level = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(MAX_SECRET+1)], default=0)

    # class Meta:
    #     db_table = 'auth_user'

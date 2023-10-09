from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    score = models.PositiveSmallIntegerField(default=0)

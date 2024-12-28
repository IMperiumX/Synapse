from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

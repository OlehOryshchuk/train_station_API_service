from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    pass

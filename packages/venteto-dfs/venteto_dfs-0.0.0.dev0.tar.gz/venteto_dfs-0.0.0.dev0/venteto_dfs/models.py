from django.contrib.auth.models import AbstractUser
from django.db.models import UUIDField
from uuid6 import uuid7


class AuthUser(AbstractUser):
    uuid = UUIDField(
        primary_key=True,
        editable=False, 
        default=uuid7,
        verbose_name="UUID v7"
    )

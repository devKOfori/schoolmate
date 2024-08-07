from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

ACCOUNT_TYPE_CHOICES = [
    ("Staff", "Staff"),
    ("Tenant", "Tenant"),
]


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    account_type = models.CharField(
        max_length=255, choices=ACCOUNT_TYPE_CHOICES, default="Staff"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "customuser"

    def __str__(self):
        return self.email

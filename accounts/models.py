from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("OWNER", "Owner"),
        ("CUSTOMER", "Customer"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CUSTOMER")
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.username
